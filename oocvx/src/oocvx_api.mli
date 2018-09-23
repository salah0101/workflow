(*---------------------------------------------------------------------------
  Copyright (c) 2017 Valentin Reis. All rights reserved.
  Distributed under the ISC license, see terms at the end of the file.
  %%NAME%% %%VERSION%%
  ---------------------------------------------------------------------------*)

(** Learning interfaces *)

(** A sequential game *)
module type Game = sig
  type context  
  type decision 
  type feedback 
  type state   
  val initial_state : state
  val decide : state -> context -> decision
  val feedback : state -> context -> feedback -> state
end

(** Supervised learning *)
module Supervised : sig
  module type API = sig
    type x 
    type y
    type model
    val initial_model : model
    val fit : model -> x -> y -> model 
    val predict : model -> x -> y      
  end

  (** Converting Between both signatures. *)
  module FromGame : functor (
    G:sig 
      type decision 
      include Game 
        with type decision:=decision 
         and type feedback=decision 
    end) 
    -> API
    with type x = G.context
     and type y = G.feedback
     and type model = G.state

  module ToGame : functor (
    S:API) 
    -> Game
    with type context = S.x
     and type feedback = S.y
     and type decision = S.y
     and type state = S.model

  module Instances : sig
    module Vector_binary_classification:sig
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
      module Mk : functor (P:Param) -> API
    end

    module Vector_regression : sig
      module type API = API
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
      module Mk : functor (P:Param) -> API 
    end

    module Vector_multi_output_regression : sig
      module type API =  API
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
      module Mk : functor (P:Param)  -> API
    end
  end
end

module WeightedSupervised : sig
  (** Weighted supervised learning *)
  module type API = sig
    type x 
    type y
    type weight
    type model
    val initial_model : model
    val fit : model -> x -> y * weight -> model 
    val predict : model -> x -> y      
  end

  (** Converting Between both signatures. *)
  module FromGame : functor (
    G:sig 
      type y 
      type weight
      include Game 
        with type decision= y
         and type feedback= y * weight
    end) 
    -> API
    with type x = G.context
     and type y = G.y
     and type weight = G.weight
     and type model = G.state

  module ToGame : functor (
    S:API) 
    -> Game
    with type context = S.x
     and type feedback = S.y * S.weight
     and type decision = S.y
     and type state = S.model
  module Instances :sig
    module type Binary_classification = API
      with type x = float list
       and type y = bool
       and type weight = float * float
  end

end

module Ranking :sig
  module type API = sig
    type x
    type model
    val initial_model : model
    val fit : model -> (x * x) -> model 
    val predict : model -> x -> float
  end

  (** Converting Between both signatures. *)
  module FromGame : functor (
    G:sig 
      type y 
      include Game 
        with type decision=float
         and type feedback=y
         and type context=y
    end) 
    -> API
    with type x = G.context
     and type model = G.state

  module ToGame : functor (
    S:API) 
    -> Game
    with type context = S.x
     and type feedback = S.x
     and type decision = float
     and type state = S.model

  module Instances : sig 
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
