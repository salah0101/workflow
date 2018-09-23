(*---------------------------------------------------------------------------
  Copyright (c) 2017 Valentin Reis. All rights reserved.
  Distributed under the ISC license, see terms at the end of the file.
  %%NAME%% %%VERSION%%
  ---------------------------------------------------------------------------*)

module type Game = sig
  type context  
  type decision 
  type feedback 
  type state   
  val initial_state : state
  val decide : state -> context -> decision
  val feedback : state -> context -> feedback -> state
end

module Supervised = struct
  module type API = sig
    type x 
    type y
    type model
    val initial_model : model
    val fit : model -> x -> y -> model 
    val predict : model -> x -> y      
  end

  module FromGame (G:sig 
      type decision 
      include Game 
        with type decision:=decision 
         and type feedback=decision 
    end) = struct
    type x = G.context
    type y = G.decision 
    type model = G.state
    let initial_model = G.initial_state
    let fit = G.feedback
    let predict = G.decide 
  end

  module ToGame (S:API) = struct
    type context = S.x
    type feedback = S.y
    type decision = S.y
    type state = S.model
    let initial_state = S.initial_model
    let feedback = S.fit
    let decide = S.predict
  end

  module Instances = struct
    module Vector_binary_classification = struct
      module type API = API 
        with type x = float list
         and type y = bool

      module type Param = sig
        module Upd : Oocvx_algorithms.Update
          with type y = bool
           and type w = float list
        module Decision : Oocvx_decision.Decision
          with type x = float list
           and type y = bool
           and type w = float list
      end
      module Mk (P:Param) = struct
        type x = float list
        type y = bool
        type model = P.Upd.model
        let fit model x y = P.Upd.descent model ~x:x y
        let predict model x = P.Decision.decision (P.Upd.get_w model) x
        let initial_model = P.Upd.initial_model
      end
    end

    module Vector_regression = struct
      module type API  = API 
        with type x = float list
         and type y = float
      module type Param = sig
        module Upd : Oocvx_algorithms.Update
          with type y = float
           and type w = float list
        module Decision : Oocvx_decision.Decision
          with type x = float list
           and type y = float
           and type w = float list
      end
      module Mk (P:Param) = struct
        type x = float list
        type y = float
        type model = P.Upd.model
        let fit model x y = P.Upd.descent model ~x:x y
        let predict model x = P.Decision.decision (P.Upd.get_w model) x
        let initial_model = P.Upd.initial_model
      end
    end

    module Vector_multi_output_regression = struct
      module type API = API 
        with type x = float list
         and type y = float list
      module type Param = sig
        module Upd : Oocvx_algorithms.Update
          with type y = float list
           and type w = (float list) list
        module Decision : Oocvx_decision.Decision
          with type x = float list
           and type y = float list
           and type w = (float list) list
      end
      module Mk (P:Param) = struct
        type x = float list
        type y = float list
        type model = P.Upd.model
        let fit model x y = P.Upd.descent model ~x:x y
        let predict model x = P.Decision.decision (P.Upd.get_w model) x
        let initial_model = P.Upd.initial_model
      end
    end
  end
end

module WeightedSupervised = struct
  module type API = sig
    type x 
    type y
    type weight
    type model
    val initial_model : model
    val fit : model -> x -> y * weight -> model 
    val predict : model -> x -> y      
  end

  module FromGame (G:sig 
      type y 
      type weight
      include Game 
        with type decision= y
         and type feedback= y * weight
    end) = struct
    type x = G.context
    type y = G.y
    type weight = G.weight
    type model = G.state
    let initial_model = G.initial_state
    let fit = G.feedback
    let predict = G.decide 
  end

  module ToGame (S:API) = struct
    type context = S.x
    type feedback = S.y * S.weight
    type decision = S.y
    type state = S.model
    let initial_state = S.initial_model
    let feedback = S.fit
    let decide = S.predict
  end

  module Instances = struct
    module type Binary_classification = API
      with type x = float list
       and type y = bool
       and type weight = float * float
  end
end

module Ranking = struct
  module type API = sig
    type x
    type model
    val initial_model : model
    val fit : model -> (x * x) -> model 
    val predict : model -> x -> float
  end

  module FromGame (G:sig 
      type y 
      include Game 
        with type decision=float
         and type feedback=y
         and type context=y
    end) = struct
    type x = G.context
    type model = G.state
    let initial_model = G.initial_state
    let fit model (x,x') = G.feedback model x x'
    let predict = G.decide 
  end

  module ToGame (S:API) = struct
    type context = S.x
    type feedback = S.x
    type decision = float
    type state = S.model
    let initial_state = S.initial_model
    let feedback state context feedback = S.fit state (context, feedback)
    let decide = S.predict
  end

  module Instances = struct
    module type Vectors = API
      with type x = float list
  end
end

(*---------------------------------------------------------------------------
  Copyright (c) 2017 Valentin Reis

  Permission to use, copy, modify, and/or distribute this software for any
  purpose with or without fee is hereby granted, provided that the above
  copyright notice and this permission notice appear in all copies.

  THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
  WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
  MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
  ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
  WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
  ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
  OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
  ---------------------------------------------------------------------------*)

