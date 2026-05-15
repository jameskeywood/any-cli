{
  description = "CLI for LLM providers";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
  }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        pkgs = import nixpkgs {
          inherit system;
        };

        python = pkgs.python312;

        pythonEnv = python.withPackages (ps:
          with ps; [
            httpx
            pydantic
            pydantic-settings
            python-dotenv
            rich
            prompt-toolkit
            typer
          ]);
      in {
        devShells.default = pkgs.mkShell {
          packages = [
            pythonEnv
          ];
        };
      }
    );
}
