(*---------------------------------------------------------------------------
 Copyright (c) 2017 Valentin Reis. All rights reserved.
 Distributed under the ISC license, see terms at the end of the file.
 %%NAME%% %%VERSION%%
 ---------------------------------------------------------------------------*)

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

module Positive = struct
  type x = float list
  type y = bool
  type w = float list
  let decision w x = Oocvx_numerical.dot w x >= 0.
end

module Identity = struct
  type x = float list
  type y = float 
  type w = float list
  let decision w x = Oocvx_numerical.dot w x
end

module Identity_multiple = struct
  type x = float list
  type y = float list
  type w = (float list) list
  let decision w x = List.map (fun wi -> Oocvx_numerical.dot wi x) w
end

module Argmin = struct
  type x = float list
  type y = int 
  type w = (float list) list
  let min_pos li =
    let rec min_pos = function
      | [] -> invalid_arg "min_pos"
      | [x] -> (0, x)
      | hd::tl ->
        let p, v = min_pos tl in
        if hd < v then (0, hd) else (p + 1, v)
    in fst (min_pos li)
  let decision w x = List.map (fun wi -> Oocvx_numerical.dot wi x) w |> min_pos
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
