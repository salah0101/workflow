open Cmdliner
open Oocvx

let learners =
  [
    ("svm",Classification Svm);
    ("n1svm",Classification SvmN1);
    ("logistic",Classification Logistic);
    ("logistic+l1",Classification LogisticL1);
    ("logistic+l2",Classification LogisticL2);
    ("linreg",Regression Gaussian);
    ("ridge",Regression Ridge);
    ("lasso",Regression Lasso);
    ("svmrank",Ranking Svmrank);
    ("samplemean",Pointwise Incremental);
    ("onlinemean",Pointwise Online);
  ]

let placeholder copts lr d learner tr te poly postpoly delta=
  let trc, tec = open_in tr, open_in te
  in let () = try 

  with e -> (close_in_noerr trc; close_in_noerr tec; raise e)
  in (close_in trc; close_in tec)

type copts = {
  debug : bool
}
let copts debug = { debug; }

let copts_sect = "COMMON OPTIONS"
let help_secs = [
  `S copts_sect;
  `P "These options are common to all commands.";
  `S "MORE HELP";
  `P "Use `$(mname) $(i,COMMAND) --help' for help on a single command.";`Noblank;]

let help man_format cmds topic = match topic with
  | None -> `Help (`Pager, None) (* help about the program. *)
  | Some topic ->
      let topics = "topics" :: "patterns" :: "environment" :: cmds in
      let conv, _ = Cmdliner.Arg.enum (List.rev_map (fun s -> (s, s)) topics)
      in match conv topic with
      | `Error e -> `Error (false, e)
      | `Ok t when t = "topics" -> List.iter print_endline topics; `Ok ()
      | `Ok t when List.mem t cmds -> `Help (man_format, Some t)
      | `Ok t ->
          let page = (topic, 7, "", "", ""), [`S topic; `P "Say something";]
          in `Ok (Cmdliner.Manpage.print man_format Format.std_formatter page)

let copts_t =
  let docs = copts_sect
  in let debug =
    let doc = "Give debug output."
    in Arg.(value & flag & info ["debug"] ~docs ~doc)
    in Term.(const copts $ debug )

let help_cmd =
  let topic =
    let doc = "The topic to get help on. `topics' lists the topics." in
    Arg.(value & pos 0 (some string) None & info [] ~docv:"TOPIC" ~doc)
    in
  let doc = "display help about cvxd and cvxd commands" in
  let man =
    [`S "DESCRIPTION";
     `P "Prints help about cvxd commands and other subjects..."] @ help_secs
  in
    Term.(ret
            (const help $ Term.man_format $ Term.choice_names $topic)),
    Term.info "help" ~doc ~man

let batch_cmd =
  let docs = copts_sect
  and learner_types = String.concat ", " (List.map fst learners)
  in let delta =
    let doc = "Delta hyperparameter. Useful for rankers only."
    in Arg.(value & opt float 1. & info ["delta"] ~docv:"DELTA" ~doc)
  in let postpolynomial =
    let doc = "Use post-polynomial feature mapping. Useful for rankers only."
    in Arg.(value & flag & info ["postpolynomial"; "pp"] ~doc)
  in let polynomial =
    let doc = "Use polynomial feature mapping."
    in Arg.(value & flag & info ["polynomial"; "p"] ~doc)
  in let lambda =
    let doc = "Learning Rate."
    in Arg.(value & opt float 1. & info ["learningrate"; "l"] ~docv:"LEARNINGRATE" ~doc)
  and dimension =
    let doc = "Input dimension." in
    Arg.(value & opt int 1 & info ["dimension"; "d"] ~docv:"DIMENSION" ~doc)
  and learner =
    let doc = "Learner type in"^learner_types in
    Arg.(required & pos 0 (some (enum learners)) None & info [] ~docv:"LEARNER" ~doc)
  and csv_train_in =
    let doc = "Input training csv file." in
    Arg.(required & pos 1 (some file) None & info [] ~docv:"CSVTRAIN" ~doc)
  and csv_test_in =
    let doc = "Input testing csv file." in
    Arg.(required & pos 2 (some file) None & info [] ~docv:"CSVTEST" ~doc)
  and doc = "Run ocvxd once on a file containing some data."
  in let man =
    [`S "DESCRIPTION";
     `P doc] @ help_secs
  in
    Term.(const placeholder 
    $ copts_t 
    $ lambda 
    $ dimension 
    $ learner 
    $ csv_train_in 
    $ csv_test_in 
    $ polynomial
    $ postpolynomial
    $ delta),
    Term.info "batch" ~doc ~sdocs:docs ~man

let cmds = [batch_cmd;  help_cmd]

let default_cmd =
  let doc = "ocvxd, The Online ConVeX learning Daemon." in
  let man = help_secs in
  Term.(ret (const  (`Help (`Pager, None)) )),
    Term.info "ocvxd" ~version:"0.1" ~sdocs:copts_sect ~doc ~man

let () =
  match Term.eval_choice default_cmd cmds with
    | `Error _ -> exit 1 | _ -> exit 0
