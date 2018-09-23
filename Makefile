#Runs the experiments in the current environment.
.PHONY:all
all:
	zymake -l localhost zymakefile_fixed

#Runs the experiments in the current environment slowly.
.PHONY:slow
slow:
	zymake zymakefile_fixed

#Runs the experiments inside their environment.
.PHONY:nix-build
nix-build:
	nix-build -A opt

#Enters the environment for the experiments
.PHONY:nix-shell
nix-shell:
	nix-shell default.nix -A opt

.PHONY:clean
clean:
	rm -rf o/
	rm -rf logs
	mkdir logs

.PHONY:jupyter
jupyter:
	nix-shell default.nix -A jupyter
