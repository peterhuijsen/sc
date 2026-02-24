#!/bin/env python3
import subprocess
import sys
import unittest
from hashlib import sha256
from pathlib import Path

# Find the student's script
try:
	SCRIPT = next(Path(__file__).parent.glob("s*.py")).absolute()
except StopIteration:
	sys.stderr.write("Could not find student program. It should be named sXXXXXXXXX.py (with X replaced by the student number)\n")
	sys.exit(1)
print(f"Program found: {SCRIPT}")

# You can change this to whatever directory contains all the levels on your machine
LEVELS_DIRECTORY = path_to_data = Path.cwd() / "levels"


class TestLevels(unittest.TestCase):
	def run_level_and_assert_results(self, level_number: int, expected_hashes: dict[str, str]) -> None:
		"""
		Run the script on the file for a specific level, and check that the script prints the correct passwords for all users.
		We do that by simply hashing the password given by the script and comparing them to their known hashes.
		:param level_number: Which level to test.
		:param expected_hashes: For each user, what is the hash of their password.
		"""
		# We run the student program in a subprocess, capturing the output
		level_input = Path(LEVELS_DIRECTORY) / f"level{level_number}" / f"level{level_number}.csv"
		subprocess_result = subprocess.run(["python3", str(SCRIPT), str(level_number), str(level_input.absolute())], capture_output = True, timeout = 60 * 5, check = True)
		run_output = subprocess_result.stdout.decode("utf8")

		# We collect the candidate passwords from the program's output
		candidates = {}
		for line in run_output.splitlines(keepends = False):
			try:
				username, password = line.split(",")
			except ValueError as e:
				raise Exception("Your output should contain one line per user, and each line should be username,password") from e
			username = username.strip()
			password = password.strip()
			candidates[username] = password

		# We compare the output with the expected values
		for username, expected_hash in expected_hashes.items():
			try:
				candidate_password = candidates[username]
			except KeyError:
				self.fail(f"Your output should contain a line for {username}, but that is ont the case.")
			hasher = sha256()
			hasher.update(candidate_password.encode("utf8"))
			self.assertEqual(hasher.hexdigest(), expected_hashes[username], f"You gave {candidate_password} as a candidate password for {username}, but that does not seem to be correct. Did you find the correct password?")


	# You can uncomment the following line if you don't want this test to run (for instance if you haven't solved that level yet)
	# Just remember to check you final submission!
	#@unittest.skip
	def test_level_1(self):
		self.run_level_and_assert_results(1, {"cvan-boven": "168692e97e05a1e6c2449409042ade08655d5f6f273c492954a51e430c461ed4", "yasmin87": "ab254fbd275723cb1503ad9b6df84abb9acd9bf1de86c9f598f6498d6bb63a5b", "estoffel": "ec98fb8da41fa834a16c20a557e78830fdc8f194697ce1e5134cb5465ad6eb16", "elise38": "a0d9819c456947674a4e0356dbc93efd2ca257a164b5aedb6b8430dfa8ac15aa", "matthiasjanse": "234eb90e08264ae004f89dd45e7e647af0e16f8e0a0009a12a8d94668c85e362"})

	# You can uncomment the following line if you don't want this test to run (for instance if you haven't solved that level yet)
	# Just remember to check you final submission!
	#@unittest.skip
	def test_level_2(self):
		self.run_level_and_assert_results(2, {"bloklandlara": "ce8f365467ac720e8a425754633f5daa7a94db231013b29bffd937ec4d43cb40", "liam32": "07f35b6073f5516099ce6ec3d17547887bc50f122fa778692eea4c9551db0942", "van-der-spaendoncdean": "d7f6402ae5a13c444f4a947a7a0c84d74da03aaca2e1fb69dedb047bffd07075", "bbos": "88f8c84f67ed138f6f7b5d6f45f59c5f581cfe5aa8f47e18ce4338e98d59cecb", "molenaarlars": "196b8bc52871c931d82daedd8fd5ce633b6a77b93c78d4b8f5f81b401a622da0"})

	# You can uncomment the following line if you don't want this test to run (for instance if you haven't solved that level yet)
	# Just remember to check you final submission!
	#@unittest.skip
	def test_level_3(self):
		self.run_level_and_assert_results(3, {"ahemma-van-allemanie": "68267b716159d6c532475441f3ec884d155c9cdc23d599784f0ee6dd3123cf31", "bouhuizenisabelle": "c5a3d59f5bf81a8c7cd7973f4bcadd3e77ab573c346a5d87108097ff8e464a96", "giselmeyerlisanne": "e12d3ad323946646d9d1ae74c0c7133de7fd8a119c284643fdae9a530112c92d", "lenn00": "c5a3d59f5bf81a8c7cd7973f4bcadd3e77ab573c346a5d87108097ff8e464a96", "weijtershailey": "e12d3ad323946646d9d1ae74c0c7133de7fd8a119c284643fdae9a530112c92d"})

	# You can uncomment the following line if you don't want this test to run (for instance if you haven't solved that level yet)
	# Just remember to check you final submission!
	#@unittest.skip
	def test_level_4(self):
		self.run_level_and_assert_results(4, {"Tammy84": "3e89a7fa377568b24972b7b040e5c0cf11c24b4fe259415e376766dc76bbbe2c", "Scott92": "44d76e718cb026ab1b07771cc20eddcbd168cfc2f47ecb7ba6cd6f20ca805674", "Adrian82": "2822677ddf340dd38be6b4a7ed52a07cbc98ecf9608601ce84361074578bbc2f", "Rhonda78": "845f6197af74f4d1ca77f0e7ef85edbc3b085a7fe762c8ac9395cb426637f2a0", "Sheila76": "f4def13e8ace63a36ac80d26b2ba4cbf28d5b4fdcf3455d0db355d8914c39d7b"})

	# You can uncomment the following line if you don't want this test to run (for instance if you haven't solved that level yet)
	# Just remember to check you final submission!
	#@unittest.skip
	def test_level_5(self):
		self.run_level_and_assert_results(5, {"bloklandlara": "a295f6eef282aea0cf11a3d72a54cdc23ea3ba30eda9a53c3b2fa86cf0d39209", "liam32": "023be5b03cf01998c66cb64489330cb5d5b85e354a9c54756c0144149a4f9fef", "van-der-spaendoncdean": "e011a44cf1482e35544aaa04461c189ec05995f22e67af4a1a58aa8a5b22afbb", "bbos": "e8ea9cbd1ff112c834ab79a486942aa0d7969420b34d3b6df983bcd7b55710cf", "molenaarlars": "9563a09945f0ea551912c354f4c4cb84c9c25434c480be8d2467dec271469e12"})


if __name__ == '__main__':
	unittest.main()
