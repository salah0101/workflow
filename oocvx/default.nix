with import <nixpkgs> { };
let
  callPackage = pkgs.lib.callPackageWith (pkgs // pkgs.xlibs // self);
  #ocamlCallPackage = pkgs.ocamlPackages.callPackageWith (pkgs // pkgs.xlibs // self);
in rec { 
  oocvx = pkgs.ocamlPackages.callPackage ./oocvx.nix { };
  tests = pkgs.lib.overrideDerivation oocvx (oldAttrs: {doCheck=true;}); 
}
