{ stdenv, fetchurl, ocaml, findlib, ocamlbuild, opam, ocaml_batteries, sexplib, csv, topkg , cmdliner}:

stdenv.mkDerivation rec {
	name = "oocvx-${version}";
	version = "0.0.1";
  src = ./.;

	unpackCmd = "tar xjf $src";

	buildInputs = [ ocaml findlib ocamlbuild topkg opam  ];

  propagatedBuildInputs = [ ocaml_batteries sexplib csv cmdliner ];

	inherit (topkg) buildPhase installPhase;

  doCheck = false;

	meta = {
		license = stdenv.lib.licenses.isc;
		homepage = https://github.com/freuk/oocvx;
		description = "OCaml online convex optimization";
		inherit (ocaml.meta) platforms;
	};
}
