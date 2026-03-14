import os
import fitz
import argparse

# 引数で指定されたページ範囲の文字列を解析してページ番号リストを返す
# 例えば、"2,4,6-8"が指定された場合は、[2,4,6,7,8]を返す
def parse_page_range(page_range_str):
	pages = set()
	parts = page_range_str.split(",")

	for part in parts:
		if "-" in part:
			start, end = part.split("-")
			pages.update(range(int(start), int(end) + 1))
		else:
			pages.add(int(part))

	return sorted(pages)


def pdf_to_png(pdf_path, page_range_str):
	# 出力ディレクトリ作成
	output_dir = "output"
	os.makedirs(output_dir, exist_ok=True)

	# PDF を開く
	pages = fitz.open(pdf_path)

	# ページ指定を解析
	if page_range_str:
		target_pages = parse_page_range(page_range_str)
	else:
		target_pages = list(range(1, len(pages)+1))

	print(f"変換対象ファイル: {pdf_path}")
	print(f"変換対象ページ: {target_pages}")

	# ファイル名
	basename_without_ext = os.path.splitext(os.path.basename(pdf_path))[0]

	# 指定ページのみ保存
	for page_num in target_pages:
		if 1 <= page_num <= len(pages):
			page = pages.load_page(page_num - 1)
			# グレースケールでpixmapを作成
#			pix = page.get_pixmap(colorspace=fitz.csGRAY)
			pix = page.get_pixmap()
			output_path = os.path.join(output_dir, f"{basename_without_ext}_{page_num:03}.png")
			pix.save(output_path)
			print(f"Saved: {output_path}")
		else:
			print(f"警告: PDF に {page_num} ページは存在しません")

	

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("f", help="pdf file path")
	parser.add_argument("-r", help="convert page. ex) 2,4,6-8")
	args = parser.parse_args()

	pdf_to_png(args.f, args.r)


