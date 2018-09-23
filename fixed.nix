{
  pkgs ? import <nixpkgs> {},
  dmnix ? import ./datamove-nix {inherit pkgs;}
}:
let
    ocs = pkgs.lib.overrideDerivation dmnix.ocs (oldAttrs : {
      src = ./ocst;
    });
    zymake = pkgs.lib.overrideDerivation dmnix.zymake (oldAttrs : {
      src = ./zymake;
    });
in
pkgs.stdenv.mkDerivation  {
      name = "zymakefile_fixed";
      src=./.;
      propagatedBuildInputs =
      with pkgs;
      with dmnix;
      [
        stdenv
        zymake
        ocs
        python3
        python35Packages.docopt
        R
        rPackages.docopt
        rPackages.ggplot2
        rPackages.dplyr
        rPackages.lubridate
        rPackages.xtable
        bc
      ];
      buildPhase = ''
        patchShebangs ./misc/strong_filter
        patchShebangs ./src/global_metrics.R
        zymake -l localhost zymakefile_fixed
      '';
      installPhase = ''
        mkdir -p $out/
        mv o/zymakefile_fixed/*.tex $out/
      '';
    }
