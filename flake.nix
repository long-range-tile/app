{
  description = "long-range-tile";

  outputs = { self, nixpkgs }: let
    pkgs = import nixpkgs {
      system = "x86_64-linux";
    };
  in {
    devShell.x86_64-linux = pkgs.mkShell {
      name = "long-range-tile";
      buildInputs = (with pkgs; [
        nodejs
        nodePackages.yarn
        nodePackages.typescript-language-server
      ]) ++ (with pkgs.python3Packages; [
        python
        virtualenv
      ]);
      shellHook = ''
        if [ ! -d ./api/venv ]; then
          virtualenv ./api/venv
          ./api/venv/bin/pip install -r ./api/requirements.txt
        fi
        source ./api/venv/bin/activate
      '';
    };
  };
}
