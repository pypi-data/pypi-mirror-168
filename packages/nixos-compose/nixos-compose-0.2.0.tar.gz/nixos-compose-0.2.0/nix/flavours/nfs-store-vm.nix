{
  name = "vm-ramdisk";
  description = "Plain vm ramdisk (all-in-memory), need lot of ram !";
  vm = true;
  image = {
    type = "ramdisk";
    distribution = "all-in-one";
  };
  module = { config, pkgs, lib, modulesPath, ... }: {
    imports = [
      #./shared/netboot.nix
      ./shared/base-vm.nix
      ./shared/stage-1-cmds.nix
      ./shared/stage-2-cmds.nix
      ./shared/common.nix
    ];
    boot.loader.grub.enable = lib.mkDefault false;

    # fileSystems."/" = {
    #   fsType = "tmpfs";
    #   options = [ "mode=0755" ];
    # };

    fileSystems."/nix/.server-ro-store" = {
      fsType = "nfs";
      device = "server:/nix/store";
      options = [ "vers=3" "nolock" "ro" "soft" "retry=10"];
      neededForBoot = true;
    };

    fileSystems."/nix/store" = {
      fsType = "overlay";
      device = "overlay";
      options = [
        "lowerdir=/nix/.ro-store:/mnt-root/nix/.server-ro-store"
        "upperdir=/nix/.rw-store/store"
        "workdir=/nix/.rw-store/work"
      ];
    };

    boot.initrd.network.enable = true;
    boot.initrd.kernelModules = [ "loop" "overlay" "nfsv3"];



    
    
  };
}
