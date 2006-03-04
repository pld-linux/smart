if not sysconf.getReadOnly():
    if not sysconf.has("channels"):
        sysconf.set(("channels", "rpm-db"),
                    {"alias": "rpm-db",
                     "type": "rpm-sys",
                     "name": "RPM Database"})

    pkgconf.setFlag("multi-version", "kernel")
    pkgconf.setFlag("multi-version", "kernel-smp")
    pkgconf.setFlag("multi-version", "kernel-grsecurity")
    pkgconf.setFlag("multi-version", "kernel-grsecurity-sound-alsa")
    pkgconf.setFlag("multi-version", "kernel-grsecurity-sound-oss")
    pkgconf.setFlag("multi-version", "kernel-grsecurity-smp")
    pkgconf.setFlag("multi-version", "kernel-grsecurity-smp-sound-alsa")
    pkgconf.setFlag("multi-version", "kernel-grsecurity-smp-sound-oss")
    pkgconf.setFlag("multi-version", "kernel-vserver")
    pkgconf.setFlag("multi-version", "kernel-vserver-drm")
    pkgconf.setFlag("multi-version", "kernel-vserver-sound-alsa")
    pkgconf.setFlag("multi-version", "kernel-vserver-sound-oss")
    pkgconf.setFlag("multi-version", "kernel-vserver-smp")
    pkgconf.setFlag("multi-version", "kernel-vserver-smp-drm")
    pkgconf.setFlag("multi-version", "kernel-vserver-smp-sound-alsa")
    pkgconf.setFlag("multi-version", "kernel-vserver-smp-sound-oss")
    pkgconf.setFlag("multi-version", "kernel-misc-kqemu")
    pkgconf.setFlag("multi-version", "kernel-video-nvidia")
    pkgconf.setFlag("multi-version", "kernel-video-spca5xx")
