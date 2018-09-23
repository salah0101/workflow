(*---------------------------------------------------------------------------
  Copyright (c) 2017 Valentin Reis. All rights reserved.
  Distributed under the ISC license, see terms at the end of the file.
  %%NAME%% %%VERSION%%
  ---------------------------------------------------------------------------*)

(** Algorithms *)

(** A model *)
module type Model = sig
  type w
  type model
  val get_w : model -> w
  val initial_model : int -> model
end

(** The output of this module hell. *)
module type Update = sig
  include Model
  type y
  val initial_model : model
  val descent : model -> x:(float list) -> y -> model
end

(** {1:algs Algorithms} *)
module Descents : sig

  (** Stochastic Gradient Descent [[1]]*)
  module SGD : sig
    module type Param = sig 
      module Reg : Oocvx_reg.Vector_derivative 
      module Loss : Oocvx_losses.Vector_derivative
      val learning_rate : float
      val dimension : int
    end
    module Model : Model
    module Mk : functor (P:Param) -> Update
      with type y = P.Loss.y
       and type model = Model.model
       and type w = float list
  end

  (** Online Gradient Descent [[2]]*)
  module OGD : sig
    module type Param = sig 
      module Proj : Oocvx_reg.Vector_projection
      module Loss : Oocvx_losses.Vector_derivative
      val learning_rate : float
      val dimension : int
    end
    module Model : Model
    module Mk : functor (P:Param) -> Update
      with type y = P.Loss.y
       and type model = Model.model
       and type w = float list
  end

  (** Normalized Gradient Descent [[3]]*)
  module NG : sig
    module type Param = sig 
      module Loss : Oocvx_losses.Vector_derivative
      val learning_rate : float
      val dimension : int
    end
    module Model : Model
    module Mk : functor (P:Param) -> Update
      with type y = P.Loss.y
       and type model = Model.model
       and type w = float list
  end

  (** Adaptive Mirror Descent [[4]]*)
  module AMD : sig
    module type Param = sig 
      module Prox : Oocvx_reg.Vector_prox
      module Loss : Oocvx_losses.Vector_derivative
      val learning_rate : float
      val dimension : int
      val eps : float
      val delta : float
    end
    module Model : Model
    module Mk : functor (P:Param) -> Update
      with type y = P.Loss.y
       and type model = Model.model
       and type w = float list
  end
end

(** {1:tools Tools} *)

(** Separate models *)
module Separate : sig 
  module type Param = sig
    module Upd : Update
    val target_dimension:int
  end
  module Mk: functor (P:Param ) 
    -> Update
    with type w = P.Upd.w list
     and type model = P.Upd.model list
     and type y = P.Upd.y list
end

(**
   {1:refs References}

   [[1]] {{:http://leon.bottou.org/papers/bottou-98x}Online Algorithms 
   and Stochastic Approximations},
   Leon Bottou

   [[2]] {{:https://people.eecs.berkeley.edu/~brecht/cs294docs/week1/03.Zinkevich.pdf}
   Online Convex Programming and Generalized Infinitesimal Gradient Ascent},
   Martin Zinkevich

   [[3]] {{:http://arxiv.org/abs/1305.6646}Normalized Online Learning},
   Stephane Ross, Paul Mineiro, John Langford

   [[4]] {{:http://jmlr.org/papers/volume12/duchi11a/duchi11a.pdf}Adaptive Subgradient
   methods for Online Learning and Stochastic Optimization},
   John Duchi , Elad Hazan and Yoram Singer.

*)


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

