FROM debian:latest
RUN apt-get update && apt-get install -y openssh-server
RUN mkdir /var/run/sshd
RUN useradd tester2
RUN echo 'tester2:test2' | chpasswd
RUN mkdir -p /home/tester2/.ssh/
COPY pub_keys/key2.pub /home/tester2/.ssh/authorized_keys
RUN chown -R tester2:tester2 /home/tester2/.ssh/
RUN chmod 700 /home/tester2/.ssh/
RUN chmod 600 /home/tester2/.ssh/authorized_keys
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config
CMD ["/usr/sbin/sshd", "-D"]