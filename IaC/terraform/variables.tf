terraform {
  required_providers {
    hcloud = {
      source = "hetznercloud/hcloud"
    }
    hetznerdns = {
      source  = "timohirt/hetznerdns"
      version = "2.1.0"
    }
  }
  required_version = ">= 0.13"
}

variable "image_name" {
  default = "basel-viz"
}

variable "ip_range" {
  default = "10.0.1.0/24"
}

variable "zone" {
  default = "jstet.net"
}


variable "sub_domain" {
  default = "basel-viz"
}

variable "user_data" {
  default = <<EOF
#cloud-config

hostname: jstet-basel-viz
manage_etc_hosts: true
locale: en_US.UTF-8
timezone: Europe/Berlin


users:
- default
- name: user
  groups: sudo
  sudo: "ALL=(ALL) NOPASSWD:ALL"
  lock_passwd: true
  shell: /bin/bash
  ssh_authorized_keys:
    - ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC8UQ2oLZZmSjR0rqpnWAIWufrmNrClpsn+SHvaRmiQL3aZVPs4T9XeOOMHEK4QaU82yZjjPrftE6tOX2qOd9PMRpr9T5+hAKxjb8tT9gE8iyrHnikgbIyYw08bj7Ws0C1Qk/v0OAqxcwP7dGBwDoSArCUHHqalWHUCIYfEOKqeq1ci9G283BySqsSoyNr9eK+5//4HzJgiQ5V2bcLGwWQQL2kCpOmKToGQPMTX6vOOG9d7SMFgY9HFOZo1h5RU0MTnhfVBZwmvSrYBVOSmfNBalXsoJfQUajYzpYXvztxxjynDoAEtRh7kCru02Hqfxzfm9rtaVJGihAA1CyLrJbJaXDGyahNcEFalltYJ9ZySc5MURUhUBhtw5J3j/84dWkuzLItGSk3UFybKTpB0n6Apb4Iyk3BW30Bch7nKIV0dZwljQF1Y8xWEY1Re0MV8SCAQT0Ub0btWevKfYjYT1nStVu+ay1W7Cd1JOXLTcVSzIcTExfLUJdJX2wn5heQQikc= jstet@laptop

EOF
}
