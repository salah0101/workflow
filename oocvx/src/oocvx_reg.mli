(*---------------------------------------------------------------------------
 Copyright (c) 2017 Valentin Reis. All rights reserved.
 Distributed under the ISC license, see terms at the end of the file.
 %%NAME%% %%VERSION%%
 ---------------------------------------------------------------------------*)

(** Regularizers *)

module type Base = sig type w end
module type Derivative = sig
  include Base
  val derivative: w -> w
end
module type Projection = sig
  include Base
  val projection : w -> w
end
module type Proximal = sig
  include Base
  val prox : u:w -> h:w -> delta:float -> w
end
module type Vector_derivative = Derivative with type w = float list
module type Vector_projection = Projection with type w = float list
module type Vector_prox       = Proximal   with type w = float list

module type Multiplier = sig val multiplier : float end
module type Lambda = sig include Multiplier val lambda : float end
module type Norm_dimension = sig include Multiplier val p : float end

(** $\ell_1$ regularization *)
module L1 : sig
  (** Derivative of a $\ell_1$ constraint *)
  module Vector_derivative : functor (P:Multiplier) -> Vector_derivative

  (** Projection on a $\ell_1$ ball*)
  module Vector_projection : functor (P:Multiplier) -> Vector_projection

  (** Proximal Step for a $\ell_1$ ball*)
  module Vector_prox: functor (P:Multiplier) -> Vector_prox
end

(** $\ell_2$ regularization *)
module L2 : sig
  (** Derivative of a $\ell_2$ constraint *)
  module Vector_derivative : functor (P:Multiplier) -> Vector_derivative

  (** Projection on a $\ell_2$ ball*)
  module Vector_projection : functor (P:Multiplier) -> Vector_projection

  (** Proximal Step for a $\ell_2$ ball*)
  module Vector_prox: functor (P:Multiplier) -> Vector_prox
end

(** Derivative of an elastic-net ($\left\|  \right\|_\{1\} + \lambda \left\|  \right\|_\{2\} $) constraint *)
module Elasticnet_derivative : functor (P:Lambda) -> Vector_derivative

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
