{
  description = "long-range-tile frontend";

  outputs = { self, nixpkgs }: let
    pkgs = import nixpkgs {
      system = "x86_64-linux";
    };
  in {
    devShell.x86_64-linux = pkgs.mkShell {
      name = "lrt-frontend";
      buildInputs = with pkgs; [
        nodejs
        nodePackages.yarn
      ];
    };
  };
}
