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
    zymakefile_fixed=pkgs.stdenv.mkDerivation  {
      name = "zymakefile_ft";
      buildInputs =
      with pkgs;
      [
        zymake
        ocs
        python3
        python35Packages.docopt
        R
        rPackages.docopt
        rPackages.reshape2
        rPackages.dplyr
        rPackages.ggplot2
        rPackages.xtable
        bc
      ];
    };
 
    zymakefile_ft=pkgs.stdenv.mkDerivation  {
      name = "zymakefile_ft";
      buildInputs =
      with pkgs;
      [
        zymake
        ocs
        python3
        python35Packages.docopt
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
        bc
      ];
    };
    zymakefile_classify_pure=pkgs.stdenv.mkDerivation rec {
      src = ./.;
      name="zymakefile_classify_pure";
      buildInputs =
      with pkgs;
      [
        zeromq
        dmnix.ppx_deriving_protobuf
        zymake
        ocs
        bc
        python3
        protobuf
        python35Packages.docopt
        python35Packages.vowpalwabbit
        python35Packages.pyzmq
        #python35Packages.protobuf
        python35Packages.protobuf3_2
        python35Packages.numpy
        python35Packages.pandas
        python35Packages.joblib
        python35Packages.Keras
        python35Packages.tensorflow
        python35Packages.scikitlearn
        python35Packages.matplotlib
        python35Packages.ipykernel
        python35Packages.jupyter
      ];
      buildPhase = "zymake zymakefile_classify_pure";
      installPhase = ''
        mkdir -p $out/
        mv o/zymakefile/*.final  $out/
      '';
    };
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
      ];
    };
    zymakefile_classify_bbo=pkgs.stdenv.mkDerivation rec {
      src = ./.;
      name="zymakefile_classify_bbo";
      buildInputs =
      with pkgs;
      [
        zeromq
        dmnix.ppx_deriving_protobuf
        zymake
        ocs
        bc
        python3
        protobuf
        python35Packages.docopt
        python35Packages.pyzmq
        #python35Packages.protobuf
        python35Packages.protobuf3_2
        python35Packages.numpy
        python35Packages.pandas
        python35Packages.pybrain
        python35Packages.scikitlearn
        python35Packages.matplotlib
      ];
    };
  };
in
  self
