set http_proxy=http://proxy.ign.fr:3128
set https_proxy=http://proxy.ign.fr:3128
npm config rm proxy &&  npm config set proxy %http_proxy%
npm config rm https-proxy && npm config set https-proxy %https_proxy%
