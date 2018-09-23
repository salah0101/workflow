(*---------------------------------------------------------------------------
  Copyright (c) 2017 Valentin Reis. All rights reserved.
  Distributed under the ISC license, see terms at the end of the file.
  %%NAME%% %%VERSION%%
  ---------------------------------------------------------------------------*)

(** Functional interface *)

(** {1:cl Classification} *)

(** {2:svm Binary} *)

(** {3:svm Support-Vector Machines(SVM)} *)

(** The classical way to train a SVM on a large dataset is to use 
    stochastic gradient descent. *)
val svm_sgd : 
  ?learning_rate:float
  -> ?regularization_hyperparameter:float
  -> ?dimension:int
  -> (module Oocvx_api.Supervised.Instances.Vector_binary_classification.API)

(** When regret bounds matter, online gradient descent can be used. *)
val svm_ogd : 
  ?learning_rate:float
  -> ?regularization_hyperparameter:float
  -> ?dimension:int
  -> (module Oocvx_api.Supervised.Instances.Vector_binary_classification.API)

(** Second order optimization algorithms are less sensitive to learning
    rates and changes of scale in datasets.*)
val svm_adagrad_mirror : 
  ?learning_rate:float
  -> ?eps:float
  -> ?delta:float
  -> ?regularization_hyperparameter:float
  -> ?dimension:int
  -> (module Oocvx_api.Supervised.Instances.Vector_binary_classification.API)

(** {1:cl Regression} *)

(** {3:lasso LASSO} *)

val lasso_sgd : 
  ?learning_rate:float
  -> ?regularization_hyperparameter:float
  -> ?dimension:int
  -> (module Oocvx_api.Supervised.Instances.Vector_regression.API)

(** {3:ridge Ridge Regression} *)

val ridge_sgd : 
  ?learning_rate:float
  -> ?regularization_hyperparameter:float
  -> ?dimension:int
  -> (module Oocvx_api.Supervised.Instances.Vector_regression.API)

(** {1:ridge Multi-Output Regression} *)

(** {3:ridge Ridge Regression} *)

val separate_ridge_ogd : 
  ?learning_rate:float
  -> ?regularization_hyperparameter:float
  -> ?dimension:int
  -> ?target_dimension:int
  -> (module Oocvx_api.Supervised.Instances.Vector_multi_output_regression.API)

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
