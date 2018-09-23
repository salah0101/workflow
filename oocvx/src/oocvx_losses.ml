(*---------------------------------------------------------------------------
 Copyright (c) 2017 Valentin Reis. All rights reserved.
 Distributed under the ISC license, see terms at the end of the file.
 %%NAME%% %%VERSION%%
 ---------------------------------------------------------------------------*)

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

module Hinge  = struct
  type x = float list
  type w = float list
  type y = bool 
  let derivative w x y =
    let y = if y then 1. else -.1.
    in if y *. (Oocvx_numerical.dot w x) < 1. then
      BatList.map2 (fun wi xi -> -. y *. xi) w x
    else
    BatList.make (List.length w) 0.
end

module Logistic  = struct
  type x = float list
  type w = float list
  type y = bool 
  let derivative w x y =
    let y = if y then 1. else -.1.
    in BatList.map2
      (fun xi wi ->
         -. y *. xi *. (1. -. ( 1. /. (1. +. exp ( -. y *. Oocvx_numerical.dot w x )))))
      x w
end

module Gaussian = struct 
  type x = float list
  type w = float list
  type y = float
  let derivative w x y =
    let z = Oocvx_numerical.dot w x
    in BatList.map2 (fun wi xi -> -. xi *. (y -. z)) w x
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
