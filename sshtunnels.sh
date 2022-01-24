#Access internal box:
#from kali terminal on someones internal network:
ssh root@middlebox -R 2022:localhost:22
# ^creates a tunnel at externally accessible middlebox and back to kali.

# from middlebox:
ssh root@localhost -p 2022

#Your laptop at home sitting behind firewall:
ssh -t root@middlebox -L 2023:localhost:2022 ssh -p 2022 root@localhost

#Access CS or any other service running on kali from your local machine!
ssh -L 50050:localhost:50050 -p2023 root@localhost

#make sure you ssh-copy-id to allow quicker access