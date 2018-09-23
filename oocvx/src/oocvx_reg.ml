(*---------------------------------------------------------------------------
 Copyright (c) 2017 Valentin Reis. All rights reserved.
 Distributed under the ISC license, see terms at the end of the file.
 %%NAME%% %%VERSION%%
 ---------------------------------------------------------------------------*)

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

module L2 = struct
  module Vector_derivative (P:Multiplier) = struct
    type w = float list
    let derivative w = List.map (fun wi -> 2. *. P.multiplier *. wi) w
  end

  module Vector_projection (P:Multiplier) = struct
    type w = float list
    let projection w = 
      let norm = Oocvx_numerical.l2norm w 
      in if (norm <= P.multiplier )
      then w else List.map (fun wi -> P.multiplier *. wi /. norm) w
  end

  module Vector_prox (P:Multiplier) = struct
    type w = float list
    let prox ~u:u ~h:h ~delta:d = u (**TODO*)
  end
end

module L1 = struct
  module Vector_derivative (P:Multiplier) = struct
    type w = float list
    let derivative w = w (** TODO*)
  end

  module Vector_projection (P:Multiplier) = struct
    type w = float list
    let projection w = w (**TODO*)
  end

  module Vector_prox (P:Multiplier) = struct
    type w = float list
    let prox ~u:u ~h:h ~delta:d = u (**TODO*)
  end
end


module Elasticnet_derivative (P:Lambda) = struct
  type w = float list
  let derivative w = w (**TODO*)
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
