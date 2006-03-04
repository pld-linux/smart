if not sysconf.getReadOnly():
    if not sysconf.has("channels"):
        sysconf.set(("channels", "rpm-db"),
                    {"alias": "rpm-db",
                     "type": "rpm-sys",
                     "name": "RPM Database"})

    pkgconf.setFlag("multi-version", "kernel")
    pkgconf.setFlag("multi-version", "kernel-smp")
    pkgconf.setFlag("multi-version", "kernel-xen0")
    pkgconf.setFlag("multi-version", "kernel-xenU")
    pkgconf.setFlag("multi-version", "kernel-devel")
