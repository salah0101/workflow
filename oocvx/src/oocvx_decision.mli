(*---------------------------------------------------------------------------
 Copyright (c) 2017 Valentin Reis. All rights reserved.
 Distributed under the ISC license, see terms at the end of the file.
 %%NAME%% %%VERSION%%
 ---------------------------------------------------------------------------*)

(** Decision funcions *)
module type Decision = sig
  type x 
  type y 
  type w
  val decision : w -> x -> y
end

module type Vector_classification = Decision
  with type x = float list
   and type y = bool
   and type w = float list

module type Vector_regression = Decision
  with type x = float list
   and type y = float
   and type w = float list

module type Vector_multiclass_classification = Decision
  with type x = float list
   and type y = int 
   and type w = (float list) list

module type Vector_multi_output_regression = Decision
  with type x = float list
   and type y = float list
   and type w = (float list) list

(** Classify to $\text\{true\}$ if the potential function is positive or null *)
module Positive : Vector_classification

(** Identity function *)
module Identity: Vector_regression

(** Argmin *)
module Argmin: Vector_multiclass_classification

(** Multi-output-regression *)
module Identity_multiple: Vector_multi_output_regression

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
