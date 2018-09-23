#!/usr/bin/env ocaml
#use "topfind"
#require "topkg"
open Topkg

let () =
  Pkg.describe
    ~distrib:(Pkg.distrib ()) "oocvx"
  @@ fun c ->
    Ok [ Pkg.mllib "src/oocvx.mllib"; ]

