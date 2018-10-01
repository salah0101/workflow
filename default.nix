{
  
    pkgs ? import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/17.03.tar.gz") {},

  dmnix ? import ./datamove-nix {inherit pkgs;}
}:
let
  callPackage = pkgs.lib.callPackageWith (pkgs // pkgs.xlibs // self);
  self = rec {
    ocs = pkgs.lib.overrideDerivation dmnix.ocs (oldAttrs : {
      src = ./ocst;
    });
    zymake = pkgs.lib.overrideDerivation dmnix.zymake (oldAttrs : {
      src = ./zymake;
    });
    oocvx = pkgs.lib.overrideDerivation dmnix.oocvx (oldAttrs : {
      src = ./oocvx;
    });
    pb_nt = pkgs.lib.overrideDerivation pkgs.python35Packages.pybrain (oldAttrs : {
      doCheck = false;
    });
 
    zymakefile_bbo=pkgs.stdenv.mkDerivation rec {
      name="zymakefile_bbo";
      buildInputs =
      with pkgs;
      [
        zymake
        ocs
        bc
        python3
        pb_nt
        python35Packages.docopt
        python35Packages.numpy
        python35Packages.pandas
        python35Packages.scikitlearn
        python35Packages.matplotlib

        R
        rPackages.docopt
        rPackages.ggplot2
        rPackages.broom
        rPackages.dplyr
        rPackages.randomForest
        rPackages.cvTools
        rPackages.gridExtra
        rPackages.lubridate
        rPackages.directlabels
        rPackages.tidyr
        rPackages.viridis
        rPackages.scales
        rPackages.reshape2
        rPackages.RColorBrewer
        bc

      ];
    };

  };
in
  self
