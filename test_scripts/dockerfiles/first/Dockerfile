FROM debian:latest
RUN apt-get update && apt-get install -y openssh-server
RUN mkdir /var/run/sshd
RUN useradd tester
RUN echo 'tester:test1' | chpasswd
RUN mkdir -p /home/tester/.ssh/
COPY pub_keys/key1.pub /home/tester/.ssh/authorized_keys
RUN chown -R tester:tester /home/tester/.ssh/
RUN chmod 700 /home/tester/.ssh/
RUN chmod 600 /home/tester/.ssh/authorized_keys
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config
CMD ["/usr/sbin/sshd", "-D"]