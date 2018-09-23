#!/usr/bin/env ocaml
#use "topfind"
#require "topkg"
open Topkg

let () =
  Pkg.describe 
    ~distrib:(Pkg.distrib ()) "zymake" 
  @@ fun c ->
  Ok [ Pkg.bin "src/main" ~dst:"zymake" ]
