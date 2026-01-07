data "google_compute_image" "default" {
	family  = var.image_family
	project = var.image_project
}

resource "google_compute_network" "vpc" {
	name                    = "${var.project_id}-vpc"
	auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "subnet" {
	name          = "${var.project_id}-subnet"
	ip_cidr_range = "10.0.0.0/24"
	region        = var.region
	network       = google_compute_network.vpc.self_link
}

resource "google_compute_firewall" "allow_ssh" {
	name    = "${var.project_id}-allow-ssh"
	network = google_compute_network.vpc.name

	allow {
		protocol = "tcp"
		ports    = ["22"]
	}

	source_ranges = ["0.0.0.0/0"]
}

resource "google_compute_instance" "vm" {
	name         = var.instance_name
	zone         = var.zone
	machine_type = var.machine_type

	boot_disk {
		initialize_params {
			image = data.google_compute_image.default.self_link
		}
	}

	network_interface {
		network    = google_compute_network.vpc.self_link
		subnetwork = google_compute_subnetwork.subnet.self_link
		access_config {}
	}

	tags = ["http-server"]
}

