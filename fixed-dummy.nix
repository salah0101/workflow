{
  pkgs ? import <nixpkgs> {},
  dmnix ? import ./datamove-nix {inherit pkgs;}
}:
pkgs.stdenv.mkDerivation  {
      name = "zymakefile_fixed";
      src=./o;
      #phases=["installPhase"];
      buildPhase = "ls";
      installPhase = ''
        mkdir -p $out/
        mv zymakefile_fixed/*.tex $out/
      '';
    }
