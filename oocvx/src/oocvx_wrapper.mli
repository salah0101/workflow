(*---------------------------------------------------------------------------
 Copyright (c) 2017 Valentin Reis. All rights reserved.
 Distributed under the ISC license, see terms at the end of the file.
 %%NAME%% %%VERSION%%
 ---------------------------------------------------------------------------*)

  val progressiveValidation : ?print:bool -> in_channel -> in_channel -> (result, exn) BatResult.t

  val fitFromChannel : in_channel -> (result,exn) BatResult.t

  val getStats : unit -> result

module MakeLearnerProgVal (P:ProgValParam):ProgValSig
  with type result =P.result
=struct
  type result=P.result
  let progressiveValidation ?(print=false) trainChannel testChannel =
    let printer = if print then P.printer else ignore
    in try
      if print then Printf.printf "%s" "Training: ";
      P.resetStats (); ignore (P.fitFromChannel trainChannel); printer ();
      if print then Printf.printf "%s" "Testing: ";
      P.resetStats (); ignore (P.fitFromChannel testChannel); printer ();
      BatResult.Ok (P.getStats ())
    with
    | (Oocvx_learners.CorruptedModel m) as e -> BatResult.Bad e
    | e -> raise e
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
