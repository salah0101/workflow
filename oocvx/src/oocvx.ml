(*---------------------------------------------------------------------------
  Copyright (c) 2017 Valentin Reis. All rights reserved.
  Distributed under the ISC license, see terms at the end of the file.
  %%NAME%% %%VERSION%%
  ---------------------------------------------------------------------------*)

let svm_sgd
    ?learning_rate:(lr=1.)
    ?regularization_hyperparameter:(lr=1.)
    ?dimension:(d=1)
  =
  (module Oocvx_api.Supervised.Instances.Vector_binary_classification.Mk(struct
       module Upd = Oocvx_algorithms.Descents.SGD.Mk(struct
           module Reg = Oocvx_reg.L2.Vector_derivative(struct let multiplier=lr end)
           module Loss = Oocvx_losses.Hinge
           let learning_rate = lr
           let dimension = d
         end) 
       module Decision = Oocvx_decision.Positive
     end):Oocvx_api.Supervised.Instances.Vector_binary_classification.API)

let svm_ogd
    ?learning_rate:(lr=1.)
    ?regularization_hyperparameter:(lr=1.)
    ?dimension:(d=1)
  =
  (module Oocvx_api.Supervised.Instances.Vector_binary_classification.Mk(struct
       module Upd = Oocvx_algorithms.Descents.OGD.Mk(struct
           module Proj = Oocvx_reg.L2.Vector_projection(struct let multiplier=lr end)
           module Loss = Oocvx_losses.Hinge
           let learning_rate = lr
           let dimension = d
         end) 
       module Decision = Oocvx_decision.Positive
     end):Oocvx_api.Supervised.Instances.Vector_binary_classification.API)

let svm_adagrad_mirror
    ?learning_rate:(lr=1.)
    ?eps:(eps=0.000000)
    ?delta:(delta=1.)
    ?regularization_hyperparameter:(lr=1.)
    ?dimension:(d=1)
  =
  (module Oocvx_api.Supervised.Instances.Vector_binary_classification.Mk(struct
       module Upd = Oocvx_algorithms.Descents.AMD.Mk(struct
           module Prox = Oocvx_reg.L2.Vector_prox(struct let multiplier=lr end)
           module Loss = Oocvx_losses.Hinge
           let learning_rate = lr
           let dimension = d
           let eps = eps
           let delta = delta
         end) 
       module Decision = Oocvx_decision.Positive
     end):Oocvx_api.Supervised.Instances.Vector_binary_classification.API)

let lasso_sgd
    ?learning_rate:(lr=1.)
    ?regularization_hyperparameter:(lr=1.)
    ?dimension:(d=1)
  =
  (module Oocvx_api.Supervised.Instances.Vector_regression.Mk(struct
       module Upd = Oocvx_algorithms.Descents.SGD.Mk(struct
           module Reg = Oocvx_reg.L2.Vector_derivative(struct let multiplier=lr end)
           module Loss = Oocvx_losses.Gaussian
           let learning_rate = lr
           let dimension = d
         end) 
       module Decision = Oocvx_decision.Identity
     end):Oocvx_api.Supervised.Instances.Vector_regression.API)

let ridge_sgd
    ?learning_rate:(lr=1.)
    ?regularization_hyperparameter:(lr=1.)
    ?dimension:(d=1)
  =
  (module Oocvx_api.Supervised.Instances.Vector_regression.Mk(struct
       module Upd = Oocvx_algorithms.Descents.SGD.Mk(struct
           module Reg = Oocvx_reg.L2.Vector_derivative(struct let multiplier=lr end)
           module Loss = Oocvx_losses.Gaussian
           let learning_rate = lr
           let dimension = d
         end) 
       module Decision = Oocvx_decision.Identity
     end):Oocvx_api.Supervised.Instances.Vector_regression.API)

let separate_ridge_ogd
    ?learning_rate:(lr=1.)
    ?regularization_hyperparameter:(lr=1.)
    ?dimension:(d=1)
    ?target_dimension:(td=1)
  =
  let module Base_upd = Oocvx_algorithms.Descents.OGD.Mk(struct
      module Proj = Oocvx_reg.L2.Vector_projection(struct let multiplier=lr end)
      module Loss = Oocvx_losses.Gaussian
      let learning_rate = lr
      let dimension = d
    end) 
  in (module Oocvx_api.Supervised.Instances.Vector_multi_output_regression.Mk(struct
        module Upd = Oocvx_algorithms.Separate.Mk(struct
            module Upd = Base_upd
            let target_dimension=td
          end)
        module Decision = Oocvx_decision.Identity_multiple
      end):Oocvx_api.Supervised.Instances.Vector_multi_output_regression.API)

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
