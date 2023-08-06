---
doc: |
  This workflow builds Linux kernel as .deb installable packages

steps:
- name: sysinfo
  uses: linux.sysinfo

- name: repository
  uses: core.repository_prep

- name: build
  uses: linux.build_kdebs
