{ pkgs, setup, ... }: {
  nodes = {
    foo = { ... }:
      {
        environment.systemPackages = [ pkgs.taktuk ];
      };
    bar = { ... }: { };
  };
  testScript = ''
  '';
}
