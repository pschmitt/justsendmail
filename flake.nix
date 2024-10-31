{
  description = "Flake for myl IMAP CLI client and myl-discovery, compatible with multiple systems";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    myl-discovery = {
      url = "github:pschmitt/myl-discovery";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
      myl-discovery,
      ...
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};

        sendmyl = pkgs.python3Packages.buildPythonApplication {
          pname = "sendmyl";
          version = builtins.readFile ./version.txt;
          pyproject = true;

          src = ./.;

          buildInputs = [
            pkgs.python3Packages.setuptools
            pkgs.python3Packages.setuptools-scm
          ];

          propagatedBuildInputs = with pkgs.python3Packages; [
            myl-discovery.packages.${system}.myl-discovery
            rich
            rich-argparse
          ];

          meta = {
            description = "Simple lib to send mail";
            homepage = "https://github.com/pschmitt/sendmyl";
            license = pkgs.lib.licenses.gpl3Only;
            maintainers = with pkgs.lib.maintainers; [ pschmitt ];
            mainProgram = "sendmyl";
          };
        };

        devShell = pkgs.mkShell {
          name = "sendmyl-devshell";

          buildInputs = [
            pkgs.python3
            pkgs.python3Packages.setuptools
            pkgs.python3Packages.setuptools-scm
            self.packages.${system}.myl-discovery
            pkgs.python3Packages.rich
            pkgs.python3Packages.rich-argparse
          ];

          # Additional development tools
          nativeBuildInputs = [
            pkgs.gh # GitHub CLI
            pkgs.git
            pkgs.python3Packages.ipython
            pkgs.neovim
          ];

          # Environment variables and shell hooks
          shellHook = ''
            export PYTHONPATH=${self.packages.${system}.myl}/lib/python3.x/site-packages
            echo -e "\e[34mWelcome to the sendmyl development shell!\e[0m"
            # Activate a virtual environment if desired
            # source .venv/bin/activate
          '';

          # Optional: Set up a Python virtual environment
          # if you prefer using virtualenv or similar tools
          # you can uncomment and configure the following lines
          # shellHook = ''
          #   if [ ! -d .venv ]; then
          #     python3 -m venv .venv
          #     source .venv/bin/activate
          #     pip install --upgrade pip
          #   else
          #     source .venv/bin/activate
          #   fi
          # '';
        };
      in
      {
        # pkgs
        packages.justsendmail = sendmyl;
        packages.sendmyl = sendmyl;
        defaultPackage = sendmyl;

        devShells.default = devShell;
      }
    );
}
