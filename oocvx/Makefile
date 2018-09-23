.PHONY: docker
docker-build:
	docker build -t ocaml-oocvx .

docker-run:
	docker run --volume=`pwd`:/home/opam/pkg -itd --name=oocvx ocaml-oocvx /bin/bash
	docker cp ~/.ssh oocvx:/home/opam/
	docker exec -d oocvx sudo chown -R opam:opam /home/opam/.ssh
	docker attach oocvx

docker-clean:
	docker rm oocvx

nix:
	nix-build -A oocvx

#.PHONY: build
#build:
	#topkg build

#.PHONY: doc
#doc:
	#nix-shell --run "topkg doc --docflags='-g odoc_custom.cma'"

#.PHONY: docdeploy
#docdeploy:
	#rsync -r _build/doc/api.docdir/ web:/mnt/web/web/oocvx/doc
