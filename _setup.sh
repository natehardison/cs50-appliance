# Gotta start out with one of these...
sudo yum -y update

# Install the following Python packages
python_packages=(
    python-devel  # for python-crypto
    python-crypto # for installing SSH passphrases
    pexpect       # also for installing SSH passphrases
    Django        # for edX development
)

for package in ${python_packages[@]} ; do
    sudo yum -y install $package
done

# Set up git
git config --global user.name "Nate Hardison"
git config --global user.email "nate@cs.harvard.edu"
git config --global credential.helper cache
git config --global credential.helper 'cache --timeout=3600'

# Add some common aliases to .bashrc
echo "alias ..='cd ..'" >> ~/.bashrc
echo "alias e='emacs'" >> ~/.bashrc
echo "alias v='gvim'" >> ~/.bashrc


