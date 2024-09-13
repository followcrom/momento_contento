# Putting Momcon ontothe DO Box

Check Disk Usage with df:
The df command shows the amount of disk space used and available on all mounted filesystems.

Run this command:

bash
Copy code
df -h
-h: This option makes the output "human-readable," displaying sizes in GB, MB, etc.

VBofe uplaoding momcon, the VM had:
/dev/vda1 (Main disk):
Size: 25 GB total disk space.
Used: 3.9 GB is used.
Avail: 21 GB is available.
Use%: 17% of the disk space is used.
Mounted on: / (the root directory, i.e., your main filesystem).
This is your main disk, and it shows that you have used 3.9 GB of your 25 GB total space, leaving 21 GB available.


sudo chown -R root:www-data /var/www/momento_contento


Escaped Dollar Signs:
Escaped $host, $remote_addr, and $proxy_add_x_forwarded_for in the Nginx configuration to prevent shell interpretation errors.

Post install

/dev/vda1        25G  4.0G   21G  17% /


which gunicorn

systemctl status momcon

sudo journalctl -u momcon.service