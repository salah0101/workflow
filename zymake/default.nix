with import <nixpkgs> {};
with import (../../datamove-nix) {};
stdenv.lib.overrideDerivation zymake (oldAttrs : {
  src = ./.;
})
