{
  description = "long-range-tile backend";

  outputs = { self, nixpkgs }: let
    pkgs = import nixpkgs {
      system = "x86_64-linux";
    };
  in {
    devShell.x86_64-linux = pkgs.mkShell {
      name = "lrt-backend";
      buildInputs = with pkgs.python3Packages; [
        python
        flask
      ];
    };
  };
}
