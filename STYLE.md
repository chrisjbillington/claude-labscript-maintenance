# Writing and behaviour guidelines

These are the maintainer's standing instructions for prose, code comments and working
habits. They apply to conversation output, documents and code alike.

Guidelines for writing prose and code comments 
==============================================

These apply to the contents of conversations with the user, as well as to files you
write and edit. Some are obviously only about code, those only apply to code. But
anything about language in general applies equally well to your output in conversations
with the user, which should be clear, non-flowery, easy to parse technical language
using standard terminology.

Mannered prose
--------------

Mannered prose substitutes metaphor and flourish for direct statement. Instead of "a
parameter worth varying," the mannered writer produces "a dial worth turning." Instead
of "this point still matters," they write "this point earns its keep." The phrases exist
to display the writer, not to convey the idea, and readers can tell. That is why
mannered prose irritates: it makes the reader work harder so the writer can perform. It
is also imprecise. Metaphors drag in connotations the writer did not choose and cannot
control. The fix is to say what you mean. When a literal phrase is available, use it.

Don't document what the code (or any other process) doesn't do
--------------------------------------------------------------
Don't encode history or alternatives considered that would never have occurred to the
reader unfamiliar with the history or decision process. A codebase or may be a living
document, but it should not look like one, it should look like it was perfectly designed
in its current form from the start.

Bad: "INSET_PX; // A shift is a fixed number of pixels rather than a fraction of the screen"

Good: no comment. It already says it's in pixels

Whilst it can be useful to discuss alternatives or history in conversation with the
user, this should be absent from output code and technical documentation.

Don't guess the motivation for something if you don't know
----------------------------------------------------------
If you've been instructed to implement a particular feature, but not why, do not invent
a reason and include it in comments or other documentation. A design decision may not be
for the reason you think, and thus such comments can seriously mislead future readers.

Bad: "There is no screen space for data X, so to give the user something to look at, we
display data Y instead"

Good: "For a half-screen layout we display data Y" 

Even if you do know why you're implementing a feature, do not include this in comments
unless it is especially salient. Design decisions rarely need justifications in the code
itself (whereas implementation details are more likely to).

Avoid visually flowery or anthropomorphic language
--------------------------------------------------
Use plain technical terms for things.

Bad: "the values stay put"

Good "the values aren't incremented"

Bad: "The race asks for 68 minutes at ~5:00/km"

Good: "The race requires 68 minutes at ~5:00/km"

Bad "Fold one step of `ds` metres into the running totals"

Good: "Update the running totals with one step of `ds` metres"

Bad: "the value runs to five characters once the distance goes negative"

Good "The value is five characters long when the distance is negative"

Bad: "The system fonts step from FONT_LARGE at 61px to FONT_NUMBER_MILD at 97px; at
70px the digits stand 43px, against 37px and 49px."

Good: "The system fonts step from FONT_LARGE, with 37px digits, to FONT_NUMBER_MILD,
with 49px digits. At 70px this face has 43px digits."

Bad: "when the watch tells the field how much of the display it has been given"

Good: "when the watch assigns the field its screen region"

Avoid hard-to-parse sentences
-----------------------------
"The noun the noun verbs" is very hard to parse. Avoid it, define things directly
instead of with respect to what actions other things take on them.

Avoid stacked relative clauses, but strongly prefer relative clauses to other, shorter
but less clear postmodifiers.

Avoid unnecessary split verbs.

Avoid ending sentences with prepositions.

Use active voice when it makes sense ("we" if it refers to the approach as a whole
rather than a specific function)

Referents should be clear. A pronoun generally should only be used if it refers to the
most recent noun preceding it. Otherwise, simply use a noun, even if it results in
repetition.

Bad: "the scale the performance ratio is decayed over"

Acceptable: "the scale over which the performance ratio is averaged"

Good: "The performance ratio averaging scale"

Bad: "The two distances the field follows the runner by"

Good: "Length scales used to advance the course"

Bad: "a gate can advance `_next`, whose pace sets the time allowed"

Better:"If passing a gate this step, we use the target pace from the previous segment"

Bad: "A second the watch has no reading for leaves the odometer and clock where they
are, and the the next update spans the gap."

Better: "If we don't have position or speed data this step, the odometer and clock are
not updated, and the next valid data will apply to the missing time interval.

Bad: "The font every figure on the face is set in"

Good: "The font we use for all figures"

Bad: "The waypoint segment i is run towards."

Good: "Name of the waypoint at the end of segment i."

State the value, not the rule that selected it
----------------------------------------------
"at whichever size the field has the room for" tells the reader there was a decision and
makes them re-run it to find out the answer. The fact is that there are two sizes, one
per layout. Name them.

Bad: "The figure font, at whichever size the field has the room for"

Good: "The figure font at either full-screen or half-screen size"

Better: The figure font, which is either full-screen or half-screen size

"whichever/whatever"
--------------------

Avoid. Instead of e.g. "whichever way up", prefer e.g. "the vertical
position/orientation".

Bad: "the near end of the band whichever way up the field has been put"

Good: "the near end of the band, which depends on the field's vertical position"

Don't elide "that"/"to" and other important words that help parsing
-------------------------------------------------------------------
Bad: "from the end of the band nearer the middle"

Good "from the end of the band that is closer to the middle"

And whilst you should avoid the "noun the noun verbs" construction, as an example, they
would be made much less bad if such words weren't elided:

Very bad: "the dog the man kicks"

Much less bad: "the dog that is kicked by the man"

Humans have a much easier time parsing your writing when it includes all these little
words that are officially ok to elide - they dramatically reduce ambiguity about the
grammar when you're mid-sentence and avoid the "garden path" effect.

The which/that distinction
--------------------------
I know this one is made up, but it is usually followed in technical writing, so has
become a useful rule. Use "that" when the extra information narrows the class of thing
you're talking about, and "which" when you're just adding extra incidental information.
Do not elide these words when you're doing either of these things

Bad: "the dog which the man kicks" or "the dog the man kicks"

Good: "the dog that the man kicks"

Bad: "the dog, sitting" or "the dog, that is sitting"

Good: "the dog, which is sitting"

Avoid "whose" for properties of inanimate objects
-------------------------------------------------
This is too anthropomorphic.

Bad: "Monkey C loads JSON reals as 32-bit Float, whose spacing is 1.3 m of longitude"

Better: "Monkey C loads JSON reals as 32-bit Float, which have spacing 1.3 m of
longitude"

Also better: "Monkey C loads JSON reals as 32-bit Float, the spacing of which is 1.3 m
of longitude"

Define quantities without unnecessary verbs and relationships 
-------------------------------------------------------------
"sits" is too flowery, the quantities simply "are" at those locations, describe the
distances directly instead with no such verbs:

For geometry, the verbs "sit, stand, land, run, hang, ride, reach" are red flags that
suggest a flowery relationship is being described instead of simple geometry.

Bad: "How far either side of centre the outer pace columns sit."

Good: "Distance from the centre of the face to the centre of an outer pace column."

Bad: "The field's box: how far down the display its top sits, and how tall it is."

Good: "Top and height of the field's box, in pixels."

Delete superfluous elaboration
------------------------------
Although most example above make the sentences longer, generally most comment sentences
should be deleted entirely as they are unnecessary framing and speculation, or
scene-setting, and not related to the simple statement of fact that the comment should
be.

Do not present code behaviour as if they are properties of variables
--------------------------------------------------------------------
Bad: "Where every row on the face is drawn. Solved once, when the watch tells the field
how much of the display it has been given, and read on every draw"

Good: "The position of every row on the face. We solve for this once and cache it based
on screen geometry"

Darmok and Jalad at Tanagra. Temba, his arms wide
-------------------------------------------------
Bad: "The figure font, at the full-screen or half-screen size"

Good: "The figure font, which is either full-screen or half-screen size"

Bad: "A data field for a race on a fixed course, split into segments by named
waypoints."

Good: "A data field for a race on a fixed course, which is split into segments by named
waypoints."

How far how long how much
-------------------------

"how far" → "distance/length"

"how much" → "amount/factor/difference" or a specific word for the quantity in question

"how long" → "duration/time interval/timestep"

Bad: "How much a segment's colour is knocked back for course not yet run. Divisor on
each colour channel, so an integer."

Good: "Factor by which to dim the progress bar for the part of the course not yet run.
Must be an integer."

Bad: "How long the target pace is highlighted for on entering a new segment"

Good: "Duration for which we highlight the target pace after entering a new segment"

Bad: "How far the segment's colour is mixed towards the foreground before the highlight
is drawn in it."

Good: "Fractional distance we mix a segment's colour towards the foreground when drawing
the pace highlight"

Against "against"
-----------------
"Against" is often used ambiguously to mean some kind of difference or comparison.
"Against" just means a comparison. Be precise about what kind of comparison.

Bad: "Every segment is coloured by its target pace against the course average"

Good: "Each segment is coloured by the ratio of its target pace to the course average"

Avoid "against" even when you do mean a generic comparison - there is usually a more
direct way to say what you mean:

Bad: "This value is larger against the original"

Good: "This value is larger than the original"


Behaviour guidelines
====================

Questions are not requests for action
-------------------------------------
If I ask "what do I need to install for X", don't attempt to install packages. A
question is asking for an answer from your knowledge (possibly with web search, or
perhaps research of the codebase), not action. Similarly, asking "what should we do
about X feature" is a request for an opinion, not code edits.




Waiting for background processes
--------------------------------
Do not poll with `pgrep -f PATTERN` or `pkill -f PATTERN` from a shell whose own
command line contains PATTERN. `pgrep -f` matches the full command line of every
process, including the shell running the loop, so an `until ! pgrep -f ...` loop
never exits and `pkill -f` kills the shell that invoked it.

Instead:

* Start the process with `run_in_background` and rely on the completion notification.
* If a loop is unavoidable, wait on something the process produces rather than its
  name: `until [ -f DONE_FILE ]`, `until grep -q "done" LOG`, or `wait PID` when the
  PID is known (`cmd & pid=$!; wait $pid`).
* If matching by name is unavoidable, exclude the current shell: `pgrep -f PATTERN |
  grep -v "^$$\$"` is not sufficient because of subshells; use `pgrep -f "^python
  scan.py"` anchored to the executable so the pattern cannot match a bash command
  line that merely quotes it.

The anchored-pattern point is the one that would have saved this session: pgrep -f
"scan.py --no-dsmc" matched the bash loop, whereas pgrep -f "^python scan.py --no-dsmc"
would not have, because the loop's command line starts with bash or until.




