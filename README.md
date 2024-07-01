# ENPM809X Project #1: Treaps
**Due Date:** March 28, 2024, 04:00 PM

## Overview
This project explores the implementation and evaluation of the Treap data structure, which combines properties of a binary search tree and a heap. Treaps maintain nodes ordered by key values in a binary search tree manner and by priority values in a max-heap manner.

## Project Goals
- Implement functions for inserting nodes (`TreapInsert`) and searching for keys (`TreapSearch`) in a Treap.
- Build a Treap using random priorities and verify its adherence to Treap properties.
- Compare the search efficiency of Treaps with random priorities, letter frequency-based priorities, and a simple binary search tree structure.

## Tasks
### TreapInsert Function
- Inserts a new node into a Treap while maintaining Treap properties.
- Inputs: Root pointer of an existing Treap and pointer to a new node containing key and priority.
- Outputs: Root pointer of the modified Treap.

### TreapSearch Function
- Searches for a given key in the Treap and returns true if found, false otherwise.
- Inputs: Root pointer of the Treap and key value to search.

### Building the Treap
- Use `TreapInsert` to construct a Treap using uppercase letters in the specified order:
{'Z', 'Y', 'X', 'W', 'V', 'B', 'U', 'G', 'M', 'R', 'K', 'J', 'D', 'Q',
'E', 'C', 'S', 'I', 'H', 'P', 'L', 'A', 'N', 'O', 'T', 'F'}

sql
Copy code
- Use randomly generated priorities for each letter.

### File Search Program
- Develop a program that reads the file `FellowshipOfTheRing.txt` character by character.
- For each uppercase character, perform a search using `TreapSearch`.
- For each lowercase character, convert to uppercase and then search.
- Measure total search time using `gettimeofday()`.

### Priority based on Letter Frequency
- Repeat steps 3 and 4 using priorities based on the average frequency of English letters.

### Simple Binary Search Tree
- Repeat steps 3 and 4 without using priorities, effectively creating a binary search tree.

## Evaluation
- Measure and compare average search times across the three implementations (random priorities, letter frequency-based priorities, and simple BST).
- Determine if using Treaps improves search efficiency compared to a simple binary search tree.

## Submission Requirements
Submit the following at the end of the project:
- Your program (in C or Python) including `TreapInsert`, `TreapSearch` functions, and the main function; ensure it is compilable.
- A diagram showing the resulting Treap structure from step 5, including keys and priorities of all nodes.
- Average running times measured in steps 4, 5, and 6.
- Answers to questions posed in steps 5 and 6.
