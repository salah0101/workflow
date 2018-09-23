(*---------------------------------------------------------------------------
 Copyright (c) 2017 Valentin Reis. All rights reserved.
 Distributed under the ISC license, see terms at the end of the file.
 %%NAME%% %%VERSION%%
 ---------------------------------------------------------------------------*)

(** Loss functions *)
module type Derivative = sig
  type x 
  type y 
  type w
  val derivative : w -> x -> y -> w
end
module type Vector_derivative = Derivative
  with type x = float list
   and type w = float list
module type Regression_derivative = Vector_derivative with type y = float
module type Classification_derivative = Vector_derivative with type y = bool

(** {1:l Losses} *)

(** {2:l Classification}
    All losses are written with $y \in \{1,-1\}$.  *)

(** {3:l Binary} *)
 
(** Hinge Loss: $\frac\{\partial\}\{\partial w\} max(0, 1 - y (w^t x) )
    = - y x $ if $ y (w^t x) < 1 $ else $ 0 $ *)
module Hinge : Classification_derivative

(** Logistic Classification Loss *)
module Logistic : Classification_derivative

(** {2:l Regression} *)

(** Gaussian Regression Loss *)
module Gaussian: Regression_derivative

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
