(*---------------------------------------------------------------------------
  Copyright (c) 2017 Valentin Reis. All rights reserved.
  Distributed under the ISC license, see terms at the end of the file.
  %%NAME%% %%VERSION%%
  ---------------------------------------------------------------------------*)

module type Model = sig
  type w
  type model
  val get_w : model -> w
  val initial_model : int -> model
end

module type Update = sig
  include Model
  type y
  val initial_model : model
  val descent : model -> x:(float list) -> y -> model
end

module Descents = struct
  module SGD = struct
    module type Param = sig 
      module Reg : Oocvx_reg.Vector_derivative 
      module Loss : Oocvx_losses.Vector_derivative
      val learning_rate : float
      val dimension : int
    end

    module Model = struct
      type w = float list
      type model = { w : float list;
                     t : int; }
      let get_w model = model.w
      let initial_model d = {
        w = BatList.make d 0.;
        t = 0;
      };
    end

    module Mk (P:Param) = struct
      assert (P.learning_rate>0.);

      include Model
      type y = P.Loss.y
      let initial_model = initial_model P.dimension
      let descent model ~x:x y = 
        assert (List.length x = P.dimension);
        let gradient = List.map2 (fun a b -> a +. b)
            (P.Loss.derivative model.w x y)
            (P.Reg.derivative model.w)
        in { w = List.map2 (fun a b -> a -. P.learning_rate *. b) model.w gradient;
             t = model.t + 1;}
    end
  end

  module OGD = struct
    module type Param = sig 
      module Proj : Oocvx_reg.Vector_projection
      module Loss : Oocvx_losses.Vector_derivative
      val learning_rate : float
      val dimension : int
    end

    module Model = struct
      type w = float list
      type model = { w : float list;
                     t : int;}
      let get_w model = model.w
      let initial_model d = { w = BatList.make d 0.;
                              t = 0; }
    end

    module Mk (P:Param) = struct
      assert (P.learning_rate>0.);

      include Model
      type y = P.Loss.y
      let initial_model = initial_model P.dimension
      let descent model ~x:x y = 
        assert (List.length x = P.dimension);
        let gradient = P.Loss.derivative model.w x y
        in { w = List.map2 (fun a b -> a -. P.learning_rate *. b) model.w gradient
                 |> P.Proj.projection;
             t = model.t + 1;}
    end
  end

  module NG = struct
    module type Param = sig 
      module Loss : Oocvx_losses.Vector_derivative
      val learning_rate : float
      val dimension : int
    end

    module Model = struct
      type w = float list
      type model = { w : float list;
                     t : int;
                     s : float list; 
                     n : float;}
      let get_w model = model.w
      let initial_model d = {
        w = BatList.make d 0.;
        t = 0;
        s = BatList.make d 0.;
        n = 0.;
      }
    end

    module Mk (P:Param) = struct
      assert (P.learning_rate>0.);

      include Model
      type y = P.Loss.y
      let initial_model = initial_model P.dimension
      let descent model ~x:x y = 
        assert (List.length x = P.dimension);
        let w,s = 
          let rec recurse = function
          |([],[],[]) -> [],[]
          |((wi::ws),(si::ss),(xi::xs)) -> 
              let wi',si' = if ((abs_float xi)>si) then 
                  ((wi *. si *. si /. (xi *. xi)),abs_float xi) 
                else (wi,si)
              in let ws',ss' = recurse (ws,ss,xs)
              in (wi' :: ws' , si' :: ss')
          |_ -> failwith "Recursion error in the normalized gradient algorithm."
          in recurse (model.w, model.s, x)
        in let n = model.n +. BatList.fsum (List.map2 (fun xi si -> xi *. xi /. si *. si) s w)
        in let grad = P.Loss.derivative w x y
        in let grad' = BatList.map2 (fun si gi -> (float_of_int model.t) *. gi /. (n *. si *. si)) s grad
        in { w = List.map2 (fun a b -> a -. P.learning_rate *. b) w grad';
             t = model.t + 1;
             s = s;
             n = n;}
    end
  end

  module AMD = struct
    module type Param = sig 
      module Prox : Oocvx_reg.Vector_prox
      module Loss : Oocvx_losses.Vector_derivative
      val learning_rate : float
      val dimension : int
      val eps : float
      val delta : float
    end

    module Model = struct
      type w = float list
      type model = { w : float list;
                     t : int;
                     g : float list;  
                     s : float list; }
      let get_w model = model.w
      let initial_model d = {
        w = BatList.make d 0.;
        t = 0;
        g = BatList.make d 0.;
        s = BatList.make d 0.;
      }
    end

    module Mk (P:Param) = struct
      assert (P.learning_rate>0.);
      assert (P.eps>0.);
      assert (P.delta>0.);
      assert (P.dimension>0);

      include Model
      type y = P.Loss.y
      let initial_model = initial_model P.dimension
      let descent model ~x:x y = 
        assert (List.length x = P.dimension);
        let grad = P.Loss.derivative model.w x y
        in let g = List.map2 (fun gi gradi -> gradi *. gradi) model.g grad
        in let s = List.map sqrt g
        in let h = List.map (fun si -> P.eps +. si) s
        in let proxarg = 
             let hadhx = Oocvx_numerical.hadamard h x
             in List.map2 (fun gradi hi -> P.learning_rate *. gradi -. hi) grad hadhx
        in { w = P.Prox.prox proxarg h P.eps ; 
             t = model.t + 1;
             g = g;
             s = s; }
    end
  end
end

module Separate = struct
  module type Param = sig
    module Upd : Update
    val target_dimension:int
  end
  module Mk (P:Param) : Update 
    with type w = P.Upd.w list
     and type model = P.Upd.model list
     and type y = P.Upd.y list
  = struct
    type w = P.Upd.w list
    type model = P.Upd.model list
    type y = P.Upd.y list
    let get_w models = List.map P.Upd.get_w models
    let initial_model = BatList.make P.target_dimension P.Upd.initial_model
    let descent models ~x:x y = List.map2 (fun mi yi-> P.Upd.descent mi ~x:x yi) models y
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
