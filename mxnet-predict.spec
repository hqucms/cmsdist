### RPM external mxnet-predict 1.5.0.rc0.mod
#%define tag 97171b96b2b7efc78eccfbe0a0c2561a377ce153
#%define branch 1.2.1.mod3
#%define github_user cms-externals
#Source: git+https://github.com/%{github_user}/incubator-mxnet.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz
%define releasename apache-mxnet-src-%{realversion}-incubating
Source: https://hqu.web.cern.ch/hqu/tools/mxnet/apache-mxnet-src-%{realversion}-incubating.tar.gz

BuildRequires: cmake ninja ccache

Requires: OpenBLAS lapack

%prep
#%setup -q -n %{n}-%{realversion}
%setup -q -n %releasename 

%build
rm -rf build
mkdir build
cd build

export CFLAGS="-I$OPENBLAS_ROOT/include -DMXNET_THREAD_LOCAL_ENGINE=1"
export LDFLAGS="-L$OPENBLAS_ROOT/lib"

cmake -GNinja \
    -DCMAKE_CUDA_COMPILER_LAUNCHER=ccache \
    -DCMAKE_C_COMPILER_LAUNCHER=ccache \
    -DCMAKE_CXX_COMPILER_LAUNCHER=ccache \
    -DCMAKE_INSTALL_PREFIX="%{i}" \
    -DCMAKE_BUILD_TYPE=Release \
    -DUSE_CUDA=OFF \
    -DUSE_OPENCV=OFF \
    -DUSE_OPENMP=OFF \
    -DUSE_BLAS=open \
    -DUSE_MKL_IF_AVAILABLE=OFF \
    -USE_MKLDNN=ON \
    -DUSE_F16C=OFF \
    -DUSE_CPP_PACKAGE=ON \
    -DBUILD_CPP_EXAMPLES=OFF \
    ..

ninja -v %{makeprocesses} -l $(getconf _NPROCESSORS_ONLN)

%install
cd build
ninja -v %{makeprocesses} -l $(getconf _NPROCESSORS_ONLN) install

