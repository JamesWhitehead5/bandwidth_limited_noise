#generate low spatial frequency images

def gen_noise_bw(resolution: Tuple[int, int], bandwidth: Tuple[int, int]) -> np.ndarray:

  nx, ny = resolution
  fxc, fyc = bandwidth[0]/2., bandwidth[1]/2.

  fx = np.arange(-nx/2, nx/2, dtype=np.int64)
  fy = np.arange(-ny/2, ny/2, dtype=np.int64)
  FY, FX = np.meshgrid(fy, fx)

  mask = np.zeros((nx, ny), dtype=np.bool)
  mask[(FX/fxc)**2 + (FY/fyc)**2 > 1.] = True

  noise = np.exp(1j*2*np.pi*np.random.rand(nx, ny))
  noise /= np.sum(np.abs(noise))

  noise[mask] = 0.


  image = np.fft.ifft2(np.fft.ifftshift(noise), norm='ortho')
  image = np.abs(image)
  image = image/np.max(image)*(2**8-1)
  image = image.astype(np.uint8)

  return image

def gen_noise_color(resolution, bandwidth):
  return np.stack([gen_noise_bw(resolution, bandwidth) for _ in range(3)], axis=-1)

for _ in range(2):
  plt.imshow(gen_noise_color(resolution=(500, 500), bandwidth=(20, 20)))
  plt.show()
