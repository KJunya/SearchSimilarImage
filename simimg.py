import cv2
from itertools import chain, tee
from pathlib import Path
from argparse import ArgumentParser
from collections import namedtuple
from functools import reduce
from shutil import copy, copy2 
from os import remove

HashedImage = namedtuple("HashedImage", 'path hash')
SimSet = namedtuple("SimSet", 'src sims')

def d_hash(img):
	resize = lambda img: cv2.resize(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), (9, 8), interpolation = cv2.INTER_AREA)
	p_diff = lambda row: ((1 if row[i] > row[i + 1] else 0) for i in range(8))
	flatten = lambda arr2d: chain(*arr2d)
	bitstr = lambda bits: "".join(map(str, bits))
	return int(bitstr(flatten(map(p_diff, resize(img)))), 2)

def similarity(h1, h2):
	diff = lambda b1, b2: b1 ^ b2
	flip = lambda b: b ^ (2 ** 64 - 1)
	def num_1(b):
		acc = 0
		while b > 0:
			acc += b & 1
			b = b >> 1
		return acc
	return num_1(flip(diff(h1, h2))) / 64

def is_image(p, suffix = (".jpg", ".png", ".tiff", ".gif", ".jpeg", ".jpeg2000", ".bmp", ".raw", ".exr", ".hdri")):
	return p.is_file() and p.suffix.lower() in suffix

def source_paths(p):
	return ((p, ), filter(is_image, p.iterdir()))[p.is_dir()]

def target_paths(p):
	return filter(is_image, p.iterdir())

def hashed_images(ps):
	read_image = lambda p: cv2.imread(str(p))
	return map(lambda p: HashedImage(p, d_hash(read_image(p))), ps)

def search_similar_to(source, inside, threshold = 0.8):
	srcs = hashed_images(source_paths(source))
	srcs, targets = ((srcs, hashed_images(target_paths(inside))), tee(srcs))[source == inside]
	targets = tuple(targets)
	non_src_targets = lambda s, ts: filter(lambda t: s.path != t.path, ts)
	is_similar = lambda h1, h2: similarity(h1, h2) >= threshold
	similar_targets = lambda s, ts: filter(lambda t: is_similar(s.hash, t.hash), ts)
	similar_sets = lambda ss, ts: map(lambda s: SimSet(s.path, tuple(map(lambda t: t.path,  similar_targets(s, non_src_targets(s, ts))))), ss)
	only_sims_exists = lambda ss: filter(lambda s: len(s.sims) > 0, ss)
	return only_sims_exists(similar_sets(srcs, targets))

def simset_to_set(ss):
	return set((ss.src, *ss.sims))

def unique(iterable):
	return reduce(lambda acc, v: ((*acc, v), acc)[v in acc], iterable, tuple())

def group_path(dst, name = "sims"):
	sufx = lambda n: f"{name}({n})"
	n = 0
	while Path(dst, sufx(n)).exists():
		n += 1
	return Path(dst, sufx(n))

def create_group(dst, srcs):
	g = group_path(dst)
	g.mkdir()
	def cp(dst, src):
		copy2(str(src), str(dst))
		return src
	return map(lambda s: cp(g, s), srcs)

def group_sets(dst, sets, keep = False):
	srcs = unique(chain(*map(lambda s: create_group(dst, s), sets)))
	if not keep:
		tuple(map(remove, srcs))

def prepare_argpar():
	parser = ArgumentParser(description = "Search and group similar images in directory")
	parser.add_argument('source', help = "A source directory containg images or an image file")
	parser.add_argument('-i', '--in', dest = 'inside', default = None, help = "A directory containing images to compare to. If not specified, the path of source directory will be provided")
	parser.add_argument('-d', '--dst', default = None, help = "The distination where groups of similar images are created; if not specified, it will be created in the same directory as the source")
	parser.add_argument('-t', '--threshold', type = float, default = 0.8, help = "Similarity threshold")
	parser.add_argument('-k', '--keep', action = 'store_true', help = "Keep images in there directories rather than moving them to each similar group")
	return parser

def check_args(args):
	src = Path(args.source)
	def quit_on_error(cond, msg):
		if cond:
			print(f"<error!> {msg}")
			quit()
	quit_on_error(not src.exists(), f"Source file {src.name!r} does not exists!")
	quit_on_error(src.is_file() and not is_image(src), f"Source file {src.name!r} is not an image file!")
	in_ = Path(args.inside) if args.inside else (src.parent if src.is_file() else src)
	quit_on_error(not in_.exists(), f"Search target directory {in_.name!r} does not exists!")
	quit_on_error(not in_.is_dir(), f"Search target directory {in_.name!r} is not a directory!")
	dst = Path(args.dst) if args.dst else (src.parent if src.is_file() else src)
	quit_on_error(not dst.exists(), f"Group destination {dst.name!r} does not exists!")
	quit_on_error(not dst.is_dir(), f"Group destination {dst.name!r} is not a directory!")
	quit_on_error(args.threshold < 0.0 or 1.0 < args.threshold, "Threshold {t!r} is invalid!".format(t = str(args.threshold)))
	return namedtuple("CheckedArgs", 'source inside dst threshold keep')(src, in_, dst, args.threshold, args.keep)

def print_simset(ss):
	print("\n".join(map(lambda sim: "{}\n\t{}".format(str(sim.src), "\n\t".join(map(str, sim.sims))), sims)))

if __name__ == '__main__':
	args = check_args(prepare_argpar().parse_args())
	sims = search_similar_to(args.source, args.inside, args.threshold)
	sets = unique((map(lambda ss: simset_to_set(ss), sims)))
	group_sets(args.dst, sets, args.keep)
