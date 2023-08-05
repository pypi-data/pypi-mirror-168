"""
	This is the Harmony compiler.

    Copyright (C) 2020, 2021, 2022  Robbert van Renesse

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions
    are met:

    1. Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.

    2. Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in the
    documentation and/or other materials provided with the distribution.

    3. Neither the name of the copyright holder nor the names of its
    contributors may be used to endorse or promote products derived
    from this software without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
    FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
    COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
    INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
    BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
    LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
    CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
    LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
    ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
    POSSIBILITY OF SUCH DAMAGE.
"""

version = [
1,2, 2402

]

import sys
import os
import pathlib
import tempfile
import getopt
import traceback
import collections
import time
import math
import html
import queue
import functools
import json
import subprocess
import webbrowser
from typing import Any, List, NamedTuple


try:
    import pydot
    got_pydot = True
except Exception as e:
    got_pydot = False

try:
    from automata.fa.nfa import NFA
    from automata.fa.dfa import DFA
    got_automata = True
except Exception as e:
    got_automata = False

# TODO.  These should not be global ideally
files = {}              # files that have been read already
constants = {}          # constants modified with -c
used_constants = set()  # constants modified and used
modules = {}            # modules modified with -m
namestack = []          # stack of module names being compiled
node_uid = 1            # unique node identifier
silent = False          # not printing periodic status updates
lasttime = 0            # last time status update was printed
imported = {}           # imported modules
labelcnt = 0            # counts labels L1, L2, ...
labelid = 0
tlavarcnt = 0           # to generate unique TLA+ variables

def json_idx(js):
    if js["type"] == "atom":
        return json_string(js)
    return "[" + json_string(js) + "]"

def json_string(js):
    type = js["type"]
    v = js["value"]
    if type in { "bool", "int" }:
        return v
    if type == "atom":
        return '"' + v + '"'
    if type == "set":
        if v == []:
            return "{}"
        return "{ " + ", ".join([ json_string(val) for val in v]) + " }"
    if type == "dict":
        if v == []:
            return "()"
        lst = [ (json_string(js["key"]), json_string(js["value"])) for js in v ]
        if [ k for k,_ in lst ] == [ str(i) for i in range(len(v)) ]:
            return "[ " + ", ".join([ x for _,x in lst ]) + " ]" 
        return "{ " + ", ".join([ k + ": " + x for k,x in lst ]) + " }" 
    if type == "pc":
        return "PC(%s)"%v
    if type == "address":
        if v == []:
            return "None"
        return "?" + v[0]["value"] + "".join([ json_idx(kv) for kv in v[1:] ])
    if type == "context":
        return "CONTEXT(" + json_string(v["name"]) + ")"
    assert False

def brief_kv(js):
    return (brief_string(js["key"]), brief_string(js["value"]))

def brief_idx(js):
    return "[" + brief_string(js) + "]"

def brief_string(js):
    type = js["type"]
    v = js["value"]
    if type in { "bool", "int" }:
        return v
    if type == "atom":
        return json.dumps(v, ensure_ascii=False)
    if type == "set":
        if v == []:
            return "{}"
        lst = [ brief_string(val) for val in v ]
        return "{ " + ", ".join(lst) + " }"
    if type == "dict":
        if v == []:
            return "()"
        lst = [ brief_kv(kv) for kv in v ]
        keys = [ k for k,v in lst ]
        if keys == [str(i) for i in range(len(v))]:
            return "[ " + ", ".join([v for k,v in lst]) + " ]" 
        else:
            return "{ " + ", ".join([k + ": " + v for k,v in lst]) + " }" 
    if type == "pc":
        return "PC(%s)"%v
    if type == "address":
        if v == []:
            return "None"
        return "?" + v[0]["value"] + "".join([ brief_idx(kv) for kv in v[1:] ])
    if type == "context":
        return "CONTEXT(" + brief_string(v["name"]) + ")"

def brief_print_vars(d):
    print("{", end="")
    first = True
    for k, v in d.items():
        if first:
            first = False
        else:
            print(",", end="")
        print(" %s: %s"%(k, brief_string(v)), end="")
    print(" }")

def brief_print_range(start, end):
    if start == end:
        return "%d"%(start)
    if start + 1 == end:
        return "%d,%d"%(start, end)
    return "%d-%d"%(start, end)

class Brief:
    def __init__(self):
        self.tid = None
        self.name = None
        self.start = 0
        self.steps = ""
        self.interrupted = False
        self.lastmis = {}
        self.shared = {}
        self.failure = ""

    def flush(self):
        if self.tid != None:
            print("T%s: %s ["%(self.tid, self.name), end="")
            if self.steps != "":
                self.steps += ","
            self.steps += brief_print_range(self.start, int(self.lastmis["pc"]))
            print(self.steps + "] ", end="");
            brief_print_vars(self.shared);

    def print_macrostep(self, mas):
        mis = mas["microsteps"]
        if mas["tid"] != self.tid:
            self.flush()
            self.tid = mas["tid"]
            self.name = mas["name"]
            self.interrupted = False
            self.lastmis = mis[0]
            self.start = int(self.lastmis["pc"])
            if "shared" in self.lastmis:
                self.shared = self.lastmis["shared"]
            lastpc = 0
            self.steps = ""
            begin = 1
        else:
            begin = 0
        for i in range(begin, len(mis)):
            if "shared" in mis[i]:
                self.shared = mis[i]["shared"]
            if self.interrupted:
                if self.steps != "":
                    self.steps += ","
                self.steps += brief_print_range(self.start, int(self.lastmis["pc"]))
                self.start = int(mis[i]["pc"])
                self.steps += ",interrupt"
            elif "choose" in mis[i]:
                if self.steps != "":
                    self.steps += ","
                self.steps += brief_print_range(self.start, int(mis[i]["pc"]))
                self.steps += "(choose %s)"%brief_string(mis[i]["choose"])
                self.start = int(mis[i]["pc"]) + 1
            elif "print" in mis[i]:
                if self.steps != "":
                    self.steps += ","
                self.steps += brief_print_range(self.start, int(mis[i]["pc"]))
                self.steps += "(print %s)"%brief_string(mis[i]["print"])
                self.start = int(mis[i]["pc"]) + 1
            elif int(mis[i]["pc"]) != int(self.lastmis["pc"]) + 1:
                if self.steps != "":
                    self.steps += ","
                self.steps += brief_print_range(self.start, int(self.lastmis["pc"]))
                self.start = int(mis[i]["pc"])
            self.lastmis = mis[i]
            if "failure" in self.lastmis:
                self.failure = self.lastmis["failure"]
            self.interrupted = "interrupt" in self.lastmis and self.lastmis["interrupt"] == "True"

    def run(self, outputfiles, behavior):
        with open(outputfiles["hco"], encoding='utf-8') as f:
            print("Phase 5: loading", outputfiles["hco"])
            top = json.load(f)
            assert isinstance(top, dict)
            if top["issue"] == "No issues":
                behavior_parse(top, True, outputfiles, behavior);
                return True

            # print("Issue:", top["issue"])
            assert isinstance(top["macrosteps"], list)
            for mes in top["macrosteps"]:
                self.print_macrostep(mes)
            self.flush()
            print(self.failure)
            return False;

class GenHTML:
    def __init__(self):
        self.top = {}
        self.nmegasteps = 0
        self.nmicrosteps = 0
        self.nthreads = 0
        self.vardir = {}

        self.style = """
#table-wrapper {
  position:relative;
}
#table-scroll {
  height:200px;
  overflow:auto;  
}
#table-wrapper table {
  width:100%;
}
#table-wrapper table * {
  color:black;
}
#table-wrapper table thead th .text {
  position:absolute;   
  top:-20px;
  z-index:2;
  height:20px;
  width:35%;
  border:1px solid red;
}
table {
    border-collapse: collapse;
    border-style: hidden;
}
table td, table th {
    border: 1px solid black;
}

        """
        self.js = """
var boxSize = 10;
var currentTime = 0;
var totalTime = 0;
var microsteps = [];
var megasteps = []
var threads = [];
var curMegaStep = 0;
var mestable = document.getElementById("mestable");
var threadtable = document.getElementById("threadtable");
var coderow = document.getElementById("coderow");
var container = document.getElementById('table-scroll');
var currOffset = 0;
var currCloc = null;

function drawTimeLine(mes) {
  var c = mes.canvas.getContext("2d");
  c.beginPath();
  c.clearRect(0, 0, mes.canvas.width, mes.canvas.height);
  var t = mes.startTime;
  var yboxes = Math.floor((mes.nsteps + 29) / 30);
  var nsteps = mes.nsteps;
  for (var y = 0; y < yboxes; y++) {
    var xboxes = nsteps > 30 ? 30 : nsteps;
    for (var x = 0; x < xboxes; x++) {
      c.fillStyle = t < currentTime ? "orange" : "white";
      c.fillRect(x * boxSize, y * boxSize, boxSize, boxSize);
      c.rect(x * boxSize, y * boxSize, boxSize, boxSize);
      c.stroke();
      t += 1;
    }
    nsteps -= xboxes;
  }
}

function currentMegaStep() {
  if (currentTime == totalTime) {
    return microsteps[currentTime - 1].mesidx;
  }
  return microsteps[currentTime].mesidx;
}

function json_string_set(obj) {
  var result = "";
  for (var i = 0; i < obj.length; i++) {
    if (result != "") {
      result += ", ";
    }
    result += json_string(obj[i]);
  }
  return "{ " + result + " }";
}

function json_string_dict(obj) {
  if (obj.length == 0) {
    return "( )"
  }

  var islist = true;
  for (var i = 0; i < obj.length; i++) {
    if (obj[i].key.type != "int" || obj[i].key.value != i.toString()) {
      islist = false;
      break;
    }
  }

  var result = "";
  if (islist) {
    for (var i = 0; i < obj.length; i++) {
      if (i != 0) {
        result += ", ";
      }
      result += json_string(obj[i].value);
    }
    if (obj.length == 1) {
      result += ",";
    }
    return "[" + result + "]";
  }

  for (var i = 0; i < obj.length; i++) {
    if (result != "") {
      result += ", ";
    }
    var kv = obj[i];
    var k = json_string(kv.key);
    var v = json_string(kv.value);
    result += k + ": " + v;
  }
  return "{ " + result + " }";
}

function json_string_address(obj) {
  if (obj.length == 0) {
    return "None";
  }
  var result = "?" + obj[0].value;
  for (var i = 1; i < obj.length; i++) {
    result += "[" + json_string(obj[i]) + "]";
  }
  return result;
}

function json_string_context(obj) {
  var name = json_string(obj.name);
  var arg = json_string(obj.arg);
  var pc = json_string(obj.pc);
  return "CTX(" + name + "(" + arg + "):" + pc + ")";
}

function json_string(obj) {
  switch (obj.type) {
  case "bool": case "int":
    return obj.value;
    break;
  case "atom":
    return '"' + obj.value + '"';
  case "set":
    return json_string_set(obj.value);
  case "dict":
    return json_string_dict(obj.value);
  case "pc":
    return "PC(" + obj.value + ")"
  case "address":
    return json_string_address(obj.value);
  case "context":
    return json_string_context(obj.value);
  default:
    return JSON.stringify(obj);
  }
}

function stringify_vars(obj) {
  var result = "";
  for (var k in obj) {
    if (k == "result" && obj[k].type == "dict" && obj[k].value.length == 0) {
      continue;
    }
    if (result != "") {
      result += ", ";
    }
    result += k + ": " + json_string(obj[k]);
  }
  return result;
}

function convert_var(obj) {
  if (obj.type != "dict") {
    return json_string(obj);
  }
  if (obj.value.length == 0) {
    return "";
  }
  var result = {};
  for (var i = 0; i < obj.value.length; i++) {
    var kv = obj.value[i];
    var k = json_string(kv.key);
    result[k] = convert_var(kv.value);
  }
  return result;
}

function convert_vars(obj) {
  var result = {};
  for (var k in obj) {
    result[k] = convert_var(obj[k]);
  }
  return result;
}

function stackTrace(tid, trace, failure) {
  var table = threads[tid].tracetable;
  table.innerHTML = "";
  if (trace.length == 0) {
    var row = table.insertRow();
    var mcell = row.insertCell();
    mcell.innerHTML = threads[tid].name;
  }
  for (var i = 0; i < trace.length; i++) {
    var row = table.insertRow();

    var mcell = row.insertCell();
    mcell.innerHTML = trace[i].method;
    switch (trace[i].calltype) {
    case "process":
        mcell.style.color = "blue";
        break;
    case "normal":
        mcell.style.color = "black";
        break;
    case "interrupt":
        mcell.style.color = "orange";
        break;
    default:
        mcell.style.color = "red";
    }

    var vcell = row.insertCell();
    var vtext = document.createTextNode(stringify_vars(trace[i].vars));
    vcell.appendChild(vtext);
  }
  if (failure != null) {
    var row = table.insertRow();
    var fcell = row.insertCell();
    fcell.innerHTML = failure;
    fcell.colSpan = 2;
    fcell.style.color = "red";
  }
}

function addToLog(step, entry) {
  var table = megasteps[step].log;
  var row = table.insertRow();
  var mcell = row.insertCell();
  mcell.innerHTML = entry;
}

function handleClick(e, mesIdx) {
  var x = Math.floor(e.offsetX / boxSize);
  var y = Math.floor(e.offsetY / boxSize);
  currentTime = megasteps[mesIdx].startTime + y*30 + x + 1;
  run_microsteps()
}

var noloc = { file: "", line: "", code: "" };

function getCode(pc) {
  var locs = state.locations;
  while (pc >= 0) {
    s = "" + pc;
    if (locs.hasOwnProperty(s)) {
      return locs[s];
    }
    pc--;
  }
  return noloc;
}

function handleKeyPress(e) {
  switch (e.key) {
    case '0':
      currentTime = 0;
      run_microsteps();
      break;
    case 'ArrowLeft':
      if (currentTime > 0) {
        currentTime -= 1;
      }
      run_microsteps();
      break;
    case 'ArrowRight':
      if (currentTime < totalTime) {
        currentTime += 1;
      }
      run_microsteps();
      break;
    case 'ArrowUp':
      var mesidx = currentMegaStep();
      var mes = megasteps[mesidx];
      if (currentTime == mes.startTime && mesidx > 0) {
          mes = megasteps[mesidx - 1];
      }
      currentTime = mes.startTime;
      run_microsteps();
      break;
    case 'ArrowDown':
      var mesidx = currentMegaStep();
      var mes = megasteps[mesidx];
      currentTime = mes.startTime + mes.nsteps;
      if (currentTime > totalTime) {
        currentTime = totalTime;
      }
      run_microsteps();
      break;
    case 'Enter':
      if (currentTime < totalTime) {
        var cloc = getCode(microsteps[currentTime].pc);
        while (++currentTime < totalTime) {
          var nloc = getCode(microsteps[currentTime].pc);
          if (nloc.file != cloc.file || nloc.line != cloc.line || nloc.code != cloc.code) {
            break;
          }
        }
        run_microsteps();
      }
      break;
    default:
      // alert("unknown key " + e.code);
  }
}

function init_microstep(masidx, misidx) {
  var mas = state.macrosteps[masidx];
  var mis = mas.microsteps[misidx];
  var t = microsteps.length;
  if (t > 0 && microsteps[t - 1].tid != mas.tid) {
    curMegaStep++;
    megasteps[curMegaStep].startTime = t;
  }
  var mes = megasteps[curMegaStep];
  mes.nsteps++;
  microsteps[t] = {
    mesidx: curMegaStep,
    masidx: masidx,
    misidx: misidx,
    tid: parseInt(mas.tid),
    pc: parseInt(mis.pc),
    invfails: misidx == mas.microsteps.length - 1 ? mas.invfails : [],
    contexts: mas.contexts
  };

  if (mis.hasOwnProperty("npc")) {
    microsteps[t].npc = mis.npc;
  }
  else {
    microsteps[t].npc = mis.pc;
  }

  microsteps[t].code = getCode(microsteps[t].npc);

  microsteps[t].cloc = document.getElementById('C' + microsteps[t].npc);
  var npc = microsteps[t].npc - 4;
  if (npc < 0) {
    npc = 0;
  }
  microsteps[t].offset = document.getElementById('P' + npc);

  if (mis.hasOwnProperty("mode")) {
    microsteps[t].mode = mis.mode;
  }
  else {
    microsteps[t].mode = misidx == 0 ? "running" : microsteps[t-1].mode;
  }

  if (mis.hasOwnProperty("atomic")) {
    microsteps[t].atomic = mis["atomic"];
  }
  else if (misidx == 0) {
    microsteps[t].atomic = 0;
  }
  else {
    microsteps[t].atomic = microsteps[t-1].atomic;
  }

  if (mis.hasOwnProperty("readonly")) {
    microsteps[t].readonly = mis["readonly"];
  }
  else if (misidx == 0) {
    microsteps[t].readonly = 0;
  }
  else {
    microsteps[t].readonly = microsteps[t-1].readonly;
  }

  if (mis.hasOwnProperty("interruptlevel")) {
    microsteps[t].interruptlevel = mis["interruptlevel"];
  }
  else if (misidx == 0) {
    microsteps[t].interruptlevel = 0;
  }
  else {
    microsteps[t].interruptlevel = microsteps[t-1].interruptlevel;
  }

  if (mis.hasOwnProperty("choose")) {
    microsteps[t].choose = "chose " + json_string(mis["choose"]);
  }
  else {
    microsteps[t].choose = null;
  }
  if (mis.hasOwnProperty("print")) {
    microsteps[t].print = json_string(mis["print"]);
  }
  else {
    microsteps[t].print = null;
  }

  if (mis.hasOwnProperty("failure")) {
    microsteps[t].failure = mis.failure;
    microsteps[t].cloc = null;
  }
  else {
    microsteps[t].failure = null;
  }

  if (mis.hasOwnProperty("trace")) {
    microsteps[t].trace = mis.trace;
  }
  else if (misidx == 0) {
    microsteps[t].trace = [];
  }
  else {
    microsteps[t].trace = microsteps[t-1].trace;
  }

  // Update local variables
  var trl = microsteps[t].trace.length; 
  if (trl > 0 && mis.hasOwnProperty("local")) {
    // deep copy first
    microsteps[t].trace = JSON.parse(JSON.stringify(microsteps[t].trace))
    microsteps[t].trace[trl - 1].vars = mis.local;
  }

  if (mis.hasOwnProperty("shared")) {
    microsteps[t].shared = convert_vars(mis.shared);
  }
  else if (t == 0) {
    microsteps[t].shared = {};
  }
  else {
    microsteps[t].shared = microsteps[t-1].shared;
  }

  if (mis.hasOwnProperty("fp")) {
    microsteps[t].fp = mis.fp;
  }
  else if (misidx == 0) {
    microsteps[t].fp = 0;
  }
  else {
    microsteps[t].fp = microsteps[t-1].fp;
  }
  if (mis.hasOwnProperty("pop")) {
    var n = parseInt(mis.pop);
    microsteps[t].stack = microsteps[t-1].stack.slice(0,
                              microsteps[t-1].stack.length - n);
  }
  else if (misidx == 0) {
    microsteps[t].stack = [];
  }
  else {
    microsteps[t].stack = microsteps[t-1].stack;
  }
  if (mis.hasOwnProperty("push")) {
    var vals = mis.push.map(x => json_string(x));
    microsteps[t].stack = microsteps[t].stack.concat(vals);
  }
  // microsteps[t].choose = microsteps[t].stack;
}

function init_macrostep(i) {
  var mas = state.macrosteps[i];
  for (var j = 0; j < mas.microsteps.length; j++) {
    init_microstep(i, j);
  }
  for (var ctx = 0; ctx < mas.contexts.length; ctx++) {
    var tid = parseInt(mas.contexts[ctx].tid);
    threads[tid].name = mas.contexts[ctx].name;
  }
}

function dict_convert(d) {
  if (typeof d === "string") {
    return d;
  }
  result = "";
  for (var k in d) {
    if (result != "") {
      result += ", ";
    }
    result += dict_convert(k) + ":" + dict_convert(d[k]);;
  }
  return "{" + result + "}";
}

function get_shared(shared, path) {
  if (!shared.hasOwnProperty(path[0])) {
    return "";
  }
  if (path.length == 1) {
    return dict_convert(shared[path[0]]);
  }
  return get_shared(shared[path[0]], path.slice(1));
}

function get_status(ctx) {
  var status = ctx.mode;
  if (status != "terminated") {
    if (ctx.atomic > 0) {
      status += " atomic";
    }
    if (ctx.readonly > 0) {
      status += " read-only";
    }
    if (ctx.interruptlevel > 0) {
      status += " interrupts-disabled";
    }
  }
  return status;
}

function escapeHTML(s) {
  return s
     .replace(/&/g, "&amp;")
     .replace(/</g, "&lt;")
     .replace(/>/g, "&gt;")
     .replace(/"/g, "&quot;")
     .replace(/'/g, "&#039;");
}

function run_microstep(t) {
  var mis = microsteps[t];
  var mesrow = mestable.rows[mis.mesidx];
  mesrow.cells[3].innerHTML = mis.npc;

  for (var i = 0; i < vardir.length; i++) {
    mesrow.cells[i + 4].innerHTML = get_shared(mis.shared, vardir[i])
  }

  if (mis.failure != null) {
    stackTrace(mis.tid, mis.trace, mis.failure);
  }
  else if (mis.print != null) {
    stackTrace(mis.tid, mis.trace, "print " + mis.print);
    addToLog(mis.mesidx, mis.print)
  }
  else {
    stackTrace(mis.tid, mis.trace, mis.choose);
  }

  for (var ctx = 0; ctx < mis.contexts.length; ctx++) {
    var tid = parseInt(mis.contexts[ctx].tid);
    threads[tid].name = mis.contexts[ctx].name;
    threadtable.rows[tid].cells[1].innerHTML = get_status(mis.contexts[ctx]);
  }
  var mes = megasteps[mis.mesidx];
  if (t != mes.startTime + mes.nsteps - 1) {
    threadtable.rows[mis.tid].cells[1].innerHTML = get_status(mis);
  }
  threadtable.rows[mis.tid].cells[3].innerHTML = mis.stack.slice(mis.fp);

  if (mis.invfails.length > 0) {
    inv = mis.invfails[0];
    code = getCode(inv.pc);
    coderow.style.color = "red";
    coderow.innerHTML = code.file + ":" + code.line + "&nbsp;&nbsp;&nbsp;" + escapeHTML(code.code) + " (" + inv.reason + ")";
    mis.cloc = null;
  }
  else {
    coderow.style.color = "blue";
    coderow.innerHTML = mis.code.file + ":" + mis.code.line + "&nbsp;&nbsp;&nbsp;" + escapeHTML(mis.code.code);
  }

  currCloc = mis.cloc;
  currOffset = mis.offset;
}

function run_microsteps() {
  coderow.innerHTML = "";
  if (currCloc != null) {
    currCloc.style.color = "black";
    currCloc = null;
  }
  for (var i = 0; i < nmegasteps; i++) {
    mestable.rows[i].cells[3].innerHTML = "";
    for (var j = 0; j < vardir.length; j++) {
      mestable.rows[i].cells[j + 4].innerHTML = "";
    }
    megasteps[i].log.innerHTML = "";
  }
  for (var tid = 0; tid < nthreads; tid++) {
    threadtable.rows[tid].cells[1].innerHTML = "init";
    stackTrace(tid, [], null);
    threadtable.rows[tid].cells[3].innerHTML = "";
  }
  for (var t = 0; t < currentTime; t++) {
    run_microstep(t);
  }
  for (var i = 0; i < nmegasteps; i++) {
    drawTimeLine(megasteps[i]);
  }
  container.scrollTop = currOffset.offsetTop;

  if (currCloc != null) {
    currCloc.style.color = "red";
  }

  var curmes = microsteps[currentTime == 0 ? 0 : (currentTime-1)].mesidx;
  for (var mes = 0; mes < nmegasteps; mes++) {
    var row = document.getElementById("mes" + mes)
    if (mes == curmes) {
      row.style = 'background-color: #A5FF33;';
    }
    else {
      row.style = 'background-color: white;';
    }
  }

  var curtid = microsteps[currentTime == 0 ? 0 : (currentTime-1)].tid;
  for (var tid = 0; tid < nthreads; tid++) {
    var row = document.getElementById("thread" + tid)
    if (tid == curtid) {
      row.style = 'background-color: #A5FF33;';
    }
    else {
      row.style = 'background-color: white;';
    }
  }
}

// Initialization starts here

for (var tid = 0; tid < nthreads; tid++) {
  threads[tid] = {
    name: "T" + tid,
    status: "normal",
    stack: [],
    stacktrace: [],
    tracetable: document.getElementById("threadinfo" + tid)
  };
}
for (let i = 0; i < nmegasteps; i++) {
  var canvas = document.getElementById("timeline" + i);
  megasteps[i] = {
    canvas: canvas,
    startTime: 0,
    nsteps: 0,
    contexts: [],
    log: document.getElementById("log" + i)
  };
  canvas.addEventListener('mousedown', function(e){handleClick(e, i)});
}
for (var j = 0; j < state.macrosteps.length; j++) {
  init_macrostep(j);
}

currentTime = totalTime = microsteps.length;
run_microsteps();
document.addEventListener('keydown', handleKeyPress);

        """

    def file_include(self, name, f):
        with open(name, encoding='utf-8') as g:
            print(g.read(), file=f)

    def html_megastep(self, step, tid, name, nmicrosteps, width, f):
        print("<tr id='mes%d'>"%(step-1), file=f)
        print("  <td align='right'>", file=f)
        print("    %d&nbsp;"%step, file=f)
        print("  </td>", file=f)

        print("  <td>", file=f)
        print("    T%s: %s"%(tid, name), file=f, end="")
        print("  </td>", file=f)

        print("  <td>", file=f)
        time = nmicrosteps
        nrows = (time + 29) // 30
        print("    <canvas id='timeline%d' width='300px' height='%dpx'>"%(step-1, 10*nrows), file=f)
        print("    </canvas>", file=f)
        print("  </td>", file=f)

        print("  <td align='center'>", file=f);
        print("  </td>", file=f)

        for i in range(width):
          print("  <td align='center'>", file=f)
          print("  </td>", file=f)

        print("  <td>", file=f)
        print("    <table id='log%d' border='1'>"%(step-1), file=f)
        print("    </table>", file=f)
        print("  </td>", file=f)
        print("</tr>", file=f)

    def vardim(self, d):
        if isinstance(d, dict):
            if d == {}:
                return (1, 0)
            totalwidth = 0
            maxheight = 0
            for k in sorted(d.keys()):
                (w, h) = self.vardim(d[k])
                totalwidth += w
                if h + 1 > maxheight:
                    maxheight = h + 1
            return (totalwidth, maxheight)
        else:
            return (1, 0)

    def varhdr(self, d, name, nrows, f):
        q = queue.Queue()
        level = 0
        q.put((d, level))
        while not q.empty():
            (nd, nl) = q.get()
            if nl > level:
                print("</tr><tr>", file=f)
                level = nl
            if isinstance(nd, dict):
                for k in sorted(nd.keys()):
                    (w,h) = self.vardim(nd[k])
                    if k[0] == '"':
                        key = k[1:-1]
                    else:
                        key = k
                    if h == 0:
                        print("<td align='center' style='font-style: italic' colspan='%d' rowspan='%d'>%s</td>"%(w,nrows-nl,key), file=f)
                    else:
                        print("<td align='center' style='font-style: italic' colspan='%d'>%s</td>"%(w,key), file=f)
                    q.put((nd[k], nl+1))

    def html_top(self, f):
        if "macrosteps" not in self.top:
            print("<table border='1'>", file=f)
            print("  <thead>", file=f)
            print("    <tr>", file=f)
            print("      <th colspan='4' style='color:red;'>", file=f)
            print("        Issue:", self.top["issue"], file=f)
            print("      </th>", file=f)
            print("    </tr>", file=f)
            print("</table>", file=f)
            return

        (width, height) = self.vardim(self.vardir)
        print("<table border='1'>", file=f)
        print("  <thead>", file=f)
        print("    <tr>", file=f)
        print("      <th colspan='4' style='color:red;'>", file=f)
        print("        Issue:", self.top["issue"], file=f)
        print("      </th>", file=f)
        print("      <th align='center' colspan='%d'>"%width, file=f)
        print("        Shared Variables", file=f)
        print("      </th>", file=f)
        print("      <th align='center' colspan='%d'>"%width, file=f)
        print("        Output", file=f)
        print("      </th>", file=f)
        print("    </tr>", file=f)

        print("    <tr>", file=f)
        print("      <th align='center' rowspan='%d'>"%height, file=f)
        print("        Turn", file=f)
        print("      </th>", file=f)
        print("      <th align='center' rowspan='%d'>"%height, file=f)
        print("        Thread", file=f)
        print("      </th>", file=f)
        print("      <th align='center' rowspan='%d'>"%height, file=f)
        print("        Instructions Executed", file=f)
        print("      </th>", file=f)
        print("      <th align='center' rowspan='%d'>"%height, file=f)
        print("        &nbsp;PC&nbsp;", file=f)
        print("      </th>", file=f)
        self.varhdr(self.vardir, "", height, f)
        print("    </tr>", file=f)
        print("  </thead>", file=f)

        print("  <tbody id='mestable'>", file=f)
        assert isinstance(self.top["macrosteps"], list)
        nsteps = 0
        tid = None
        name = None
        nmicrosteps = 0
        for mas in self.top["macrosteps"]:
            if tid == mas["tid"]:
                nmicrosteps += len(mas["microsteps"])
            else:
                if tid != None:
                    self.html_megastep(nsteps, tid, name, nmicrosteps, width, f)
                nsteps += 1
                tid = mas["tid"]
                name = mas["name"]
                nmicrosteps = len(mas["microsteps"])
        self.html_megastep(nsteps, tid, name, nmicrosteps, width, f)
        print("  </tbody>", file=f)
        print("</table>", file=f)

    def html_botleft(self, f):
        print("<div id='table-wrapper'>", file=f)
        print("  <div id='table-scroll'>", file=f)
        print("    <table border='1'>", file=f)
        print("      <tbody>", file=f)
        alter = False;
        for pc, instr in enumerate(self.top["code"]):
            if str(pc) in self.top["locations"]:
                alter = not alter;
            print("        <tr id='P%d'>"%pc, file=f)
            print("          <td align='right'>", file=f)
            print("            <a name='P%d'>%d</a>&nbsp;"%(pc, pc), file=f)
            print("          </td>", file=f)
            print("          <td style='background-color: %s;'>"%("#E6E6E6" if alter else "white"), file=f)
            print("            <span title='%s' id='C%d'>"%(self.top["explain"][pc], pc), file=f)
            print("              %s"%instr, file=f);
            print("            </span>", file=f)
            print("          </td>", file=f)
            print("        </tr>", file=f)
        print("      </body>", file=f)
        print("    </table>", file=f)
        print("  </div>", file=f)
        print("</div>", file=f)

    # output a filename of f1 relative to f2
    def pathdiff(self, f1, f2):
        return os.path.relpath(f1, start=os.path.dirname(f2))

    def html_botright(self, f, outputfiles):
        if self.nthreads == 0:
            png = outputfiles["png"]
            if png != None:
                if png[0] == "/":
                    print("      <img src='%s' alt='DFA image'>"%png, file=f)
                else:
                    assert outputfiles["htm"] != None
                    print("      <img src='%s' alt='DFA image'>"%self.pathdiff(png, outputfiles["htm"]), file=f)
            return
        print("<table border='1'", file=f)
        print("  <thead>", file=f)
        print("    <tr>", file=f)
        print("      <th colspan='4'>Threads</th>", file=f)
        print("    </tr>", file=f)
        print("    <tr>", file=f)
        print("      <th>", file=f)
        print("        ID", file=f)
        print("      </th>", file=f)
        print("      <th>", file=f)
        print("        Status", file=f)
        print("      </th>", file=f)
        print("      <th>", file=f)
        print("        Stack Trace", file=f)
        print("      </th>", file=f)
        print("      <th>", file=f)
        print("        Stack Top", file=f)
        print("      </th>", file=f)
        print("    </tr>", file=f)
        print("  </thead>", file=f)
        print("  <tbody id='threadtable'>", file=f)
        maxtid = 0
        for i in range(self.nthreads):
            print("    <tr id='thread%d'>"%i, file=f)
            print("      <td align='center'>", file=f)
            print("        T%d"%i, file=f)
            print("      </td>", file=f)
            print("      <td align='center'>", file=f)
            print("        init", file=f)
            print("      </td>", file=f)
            print("      <td>", file=f)
            print("        <table id='threadinfo%d' border='1'>"%i, file=f)
            print("        </table>", file=f)
            print("      </td>", file=f)
            print("      <td align='left'>", file=f)
            print("      </td>", file=f)
            print("    </tr>", file=f)
        print("  </tbody>", file=f)
        print("</table>", file=f)

    def html_outer(self, f, outputfiles):
        print("<table>", file=f)
        print("  <tr>", file=f)
        print("    <td colspan='2'>", file=f)
        self.html_top(f)
        print("    </td>", file=f)
        print("  </tr>", file=f)
        print("  <tr><td></td></tr>", file=f)
        print("  <tr>", file=f)
        print("    <td colspan='2'>", file=f)
        print("      <h3 style='color:blue;'>", file=f)
        print("        <div id='coderow'>", file=f)
        print("        </div>", file=f)
        print("      </h3>", file=f)
        print("    </td>", file=f)
        print("  </tr>", file=f)
        print("  <tr><td></td></tr>", file=f)
        print("  <tr>", file=f)
        print("    <td valign='top'>", file=f)
        self.html_botleft(f)
        print("    </td>", file=f)
        print("    <td valign='top'>", file=f)
        self.html_botright(f, outputfiles)
        print("    </td>", file=f)
        print("  </tr>", file=f)
        print("</table>", file=f)

    def vardir_dump(self, d, path, index, f):
        if isinstance(d, dict) and d != {}:
            for k in sorted(d.keys()):
                index = self.vardir_dump(d[k], path + [k], index, f)
            return index
        if index > 0:
            print(",", file=f)
        print("  " + str(path), end="", file=f)
        return index + 1

    def html_script(self, f, outputfiles):
        print("<script>", file=f)
        print("var nthreads = %d;"%self.nthreads, file=f)
        print("var nmegasteps = %d;"%self.nmegasteps, file=f)
        print("var vardir = [", file=f)
        self.vardir_dump(self.vardir, [], 0, f)
        print(file=f)
        print("];", file=f)
        print("var state =", file=f)
        self.file_include(outputfiles["hco"], f)
        print(";", file=f)
        print(self.js, file=f)
        # file_include("charm.js", f)
        print("</script>", file=f)

    def html_body(self, f, outputfiles):
        print("<body>", file=f)
        self.html_outer(f, outputfiles)
        self.html_script(f, outputfiles)
        print("</body>", file=f)

    def html_head(self, f):
        print("<head>", file=f)
        print("  <meta charset='UTF-8'></meta>", file=f)
        print("  <style>", file=f)
        print(self.style, file=f)
        print("  </style>", file=f)
        print("</head>", file=f)

    def html(self, f, outputfiles):
        print("<html>", file=f)
        self.html_head(f)
        self.html_body(f, outputfiles)
        print("</html>", file=f)

    def var_convert(self, v):
        if v["type"] != "dict":
            return json_string(v)
        d = {}
        for kv in v["value"]:
            k = json_string(kv["key"])
            d[k] = self.var_convert(kv["value"])
        return d

    def dict_merge(self, vardir, d):
        for (k, v) in d.items():
            if not isinstance(v, dict):
                vardir[k] = v
            else:
                if k not in vardir:
                    vardir[k] = {}
                elif not isinstance(vardir[k], dict):
                    continue
                self.dict_merge(vardir[k], v)

    def vars_add(self, vardir, shared):
        d = {}
        for (k, v) in shared.items():
            val = self.var_convert(v)
            if val != {}:
                d[k] = val
        self.dict_merge(vardir, d)

    def run(self, outputfiles):
        # First figure out how many megasteps there are and how many threads
        lasttid = -1
        with open(outputfiles["hco"], encoding='utf-8') as f:
            self.top = json.load(f)
            assert isinstance(self.top, dict)
            if "macrosteps" in self.top:
                macrosteps = self.top["macrosteps"]
                for mas in macrosteps:
                    tid = int(mas["tid"])
                    if tid >= self.nthreads:
                        self.nthreads = tid + 1
                    if tid != lasttid:
                        self.nmegasteps += 1
                        lasttid = tid
                    self.nmicrosteps += len(mas["microsteps"])
                    for mis in mas["microsteps"]:
                        if "shared" in mis:
                            self.vars_add(self.vardir, mis["shared"])
                    for ctx in mas["contexts"]:
                        tid = int(ctx["tid"])
                        if tid >= self.nthreads:
                            self.nthreads = tid + 1

        with open(outputfiles["htm"], "w", encoding='utf-8') as out:
            self.html(out, outputfiles)

# an error state is a non-final state all of whose outgoing transitions
# point only to itself
def find_error_states(transitions, final_states):
    error_states = set()
    for s, d in transitions.items():
        if s not in final_states and all(v == s for v in d.values()):
            error_states.add(s)
    return error_states

def is_dfa_equivalent(dfa, hfa) -> bool:
    stack = []

    # Create states, where each state is renamed to an index to make each state unique
    dfa_states = [(k, v) for k, v in enumerate(list(dfa.states))]
    hfa_states = [(len(dfa_states) + k, v) for k, v in enumerate(list(hfa.states))]
    states = dfa_states + hfa_states
    n = len(states)

    # For convenience for mapping between states and indices
    idx_to_states = {k: v for k, v in states}
    dfa_state_to_idx = {v: k for k, v in dfa_states}
    hfa_state_to_idx = {v: k for k, v in hfa_states}

    dfa_final_states = {k: v for k, v in dfa_states if v in dfa.final_states}
    hfa_final_states = {k: v for k, v in hfa_states if v in hfa.final_states}
    # Collection of final states, indexed by state idx
    final_states = {**dfa_final_states, **hfa_final_states}

    # Tree-implementation of sets of states
    parents = [None] * n
    rank = [None] * n
    def make_set(q: int):
        parents[q] = q
        rank[q] = 0

    def find_set(x):
        if x != parents[x]:
            parents[x] = find_set(parents[x])
        return parents[x]

    def link(x, y):
        if rank[x] > rank[y]:
            parents[y] = x
        else:
            parents[x] = y
            if rank[x] == rank[y]:
                rank[y] += 1

    def union(p: int, q: int):
        link(find_set(p), find_set(q))


    # Create a set for each state in the 2 DFAs
    for k, _ in states:
        make_set(k)

    # Union the two initial states
    dfa_init_idx = dfa_state_to_idx[dfa.initial_state]
    hfa_init_idx = hfa_state_to_idx[hfa.initial_state]
    union(dfa_init_idx, hfa_init_idx)
    stack.append((dfa_init_idx, hfa_init_idx))

    # Traverse the stack
    while stack:
        k1, k2 = stack.pop()
        q1, q2 = idx_to_states[k1], idx_to_states[k2]
        dfa_t = dfa.transitions[q1]
        hfa_t = hfa.transitions[q2]

        # Check each common transitions
        symbols = set(dfa_t.keys()).intersection(hfa_t.keys())
        for s in symbols:
            p1 = dfa_state_to_idx[dfa_t[s]]
            p2 = hfa_state_to_idx[hfa_t[s]]

            r1 = find_set(p1)
            r2 = find_set(p2)
            # If their sets are not equivalent, then combine them
            if r1 != r2:
                union(p1, p2)
                stack.append((p1, p2))

    # Create sets of sets of states
    sets = dict()
    for k, p in enumerate(parents):
        if p in sets:
            sets[p].add(k)
        else:
            sets[p] = {k}

    # Check condition for DFA equivalence
    return all(
        all(q in final_states for q in s) or all(q not in final_states for q in s)
        for s in sets.values()
    )

def read_hfa(file, dfa, nfa):
    with open(file, encoding='utf-8') as fd:
        js = json.load(fd)
        initial = js["initial"]
        states = { "{}" }
        final = set()
        symbols = set()
        for e in js["edges"]:
            symbol = json_string(e["symbol"])
            symbols.add(symbol)
        transitions = { "{}": { s: "{}" for s in symbols } }
        for n in js["nodes"]:
            idx = n["idx"]
            states.add(idx)
            if n["type"] == "final":
                final.add(idx)
            transitions[idx] = { s: "{}" for s in symbols }
        for e in js["edges"]:
            symbol = json_string(e["symbol"])
            transitions[e["src"]][symbol] = e["dst"]

    hfa = DFA(
        states=states,
        input_symbols=symbols,
        transitions=transitions,
        initial_state=initial,
        final_states=final
    )

    print("Phase 7: comparing behaviors", len(dfa.states), len(hfa.states))
    assert dfa.input_symbols <= hfa.input_symbols
    if dfa.input_symbols < hfa.input_symbols:
        print("behavior warning: symbols missing from behavior:",
            hfa.input_symbols - dfa.input_symbols)
        return

    if is_dfa_equivalent(dfa, hfa):
        return

    print("Implementation behavior is not equivalent to Specification behavior. Checking for subset relation.")
    if len(dfa.states) > 100 or len(hfa.states) > 100:
        print("  warning: this could take a while")

    if dfa < hfa:
        print("behavior warning: strict subset of specified behavior")
        diff = hfa - dfa
        behavior_show_diagram(diff, "diff.png")
        return

# Modified from automata-lib
def behavior_show_diagram(dfa, path=None):
    graph = pydot.Dot(graph_type='digraph', rankdir='LR')
    nodes = {}
    rename = {}
    next_idx = 0
    error_states = find_error_states(dfa.transitions, dfa.final_states)
    for state in dfa.states:
        if state in rename:
            idx = rename[state]
        else:
            rename[state] = idx = next_idx
            next_idx += 1
        if state in error_states:
            continue
        if state == dfa.initial_state:
            # color start state with green
            if state in dfa.final_states:
                initial_state_node = pydot.Node(
                    str(idx),
                    style='filled',
                    peripheries=2,
                    fillcolor='#66cc33', label="initial")
            else:
                initial_state_node = pydot.Node(
                    str(idx), style='filled', fillcolor='#66cc33', label="initial")
            nodes[state] = initial_state_node
            graph.add_node(initial_state_node)
        else:
            if state in dfa.final_states:
                state_node = pydot.Node(str(idx), peripheries=2, label="final")
            else:
                state_node = pydot.Node(str(idx), label="")
            nodes[state] = state_node
            graph.add_node(state_node)
    # adding edges
    for from_state, lookup in dfa.transitions.items():
        for to_label, to_state in lookup.items():
            if to_state not in error_states and to_label != "":
                graph.add_edge(pydot.Edge(
                    nodes[from_state],
                    nodes[to_state],
                    label=to_label
                ))
    if path:
        try:
            graph.write_png(path, encoding='utf-8')
        except FileNotFoundError:
            print("install graphviz (www.graphviz.org) to see output DFAs")
    return graph

def eps_closure_rec(states, transitions, current, output):
    if current in output:
        return
    output.add(current)
    t = transitions[current]
    if '' in t:
        for s in t['']:
            eps_closure_rec(states, transitions, s, output)

def eps_closure(states, transitions, current):
    x = set()
    eps_closure_rec(states, transitions, current, x)
    return frozenset(x)

def behavior_parse(js, minify, outputfiles, behavior):
    if outputfiles["hfa"] == None and outputfiles["png"] == None and outputfiles["gv"] == None and behavior == None:
        return

    states = set()
    initial_state = None;
    final_states = set()
    transitions = {}
    labels = {}

    for s in js["nodes"]:
        idx = str(s["idx"])
        transitions[idx] = {}
        if s["type"] == "initial":
            assert initial_state == None
            initial_state = idx;
            val = "__init__"
        elif s["type"] == "terminal":
            final_states.add(idx)
        states.add(idx)

    def add_edge(src, val, dst):
        assert dst != initial_state
        # assert src not in final_states
        if val in transitions[src]:
            transitions[src][val].add(dst)
        else:
            transitions[src][val] = {dst}

    intermediate = 0
    symbols = js['symbols']
    input_symbols = { json_string(v) for v in symbols.values() }
    labels = { json_string(v):v for v in symbols.values() }
    for s in js['nodes']:
        for [path, dsts] in s["transitions"]:
            for dest_node in dsts:
                src = str(s["idx"])
                dst = str(dest_node)
                if path == []:
                    add_edge(src, "", dst)
                else:
                    for e in path[:-1]:
                        symbol = json_string(symbols[str(e)])
                        inter = "s%d"%intermediate
                        intermediate += 1
                        states.add(inter)
                        transitions[inter] = {}
                        add_edge(src, symbol, inter)
                        src = inter
                    e = path[-1]
                    symbol = json_string(symbols[str(e)])
                    add_edge(src, symbol, dst)

    # print("states", states, file=sys.stderr)
    # print("initial", initial_state, file=sys.stderr)
    # print("final", final_states, file=sys.stderr)
    # print("symbols", input_symbols, file=sys.stderr)
    # print("transitions", transitions, file=sys.stderr)

    print("Phase 6: convert NFA (%d states) to DFA"%len(states), file=sys.stderr)

    if got_automata:
        nfa = NFA(
            states=states,
            input_symbols=input_symbols,
            transitions=transitions,
            initial_state=initial_state,
            final_states=final_states
        )
        intermediate = DFA.from_nfa(nfa)  # returns an equivalent DFA
        if minify and len(final_states) != 0:
            print("minify #states=%d"%len(intermediate.states), file=sys.stderr)
            dfa = intermediate.minify(retain_names = True)
            print("minify done #states=%d"%len(dfa.states), file=sys.stderr)
        else:
            dfa = intermediate
        dfa_states = dfa.states
        (dfa_transitions,) = dfa.transitions,
        dfa_initial_state = dfa.initial_state
        dfa_final_states = dfa.final_states
    else:
        # Compute the epsilon closure for each state
        eps_closures = { s:eps_closure(states, transitions, s) for s in states }

        # Convert the NFA into a DFA
        dfa_transitions = {}
        dfa_initial_state = eps_closures[initial_state]
        q = [dfa_initial_state]       # queue of states to handle
        while q != []:
            current = q.pop()
            if current in dfa_transitions:
                continue
            dfa_transitions[current] = {}
            for symbol in input_symbols:
                ec = set()
                for nfa_state in current:
                    if symbol in transitions[nfa_state]:
                        for next in transitions[nfa_state][symbol]:
                            ec |= eps_closures[next]
                n = dfa_transitions[current][symbol] = frozenset(ec)
                q.append(n)
        dfa_states = set(dfa_transitions.keys())
        dfa_final_states = set()
        for dfa_state in dfa_states:
            for nfa_state in dfa_state:
                if nfa_state in final_states:
                    dfa_final_states.add(dfa_state)
        print("conversion done")
    dfa_error_states = find_error_states(dfa_transitions, dfa_final_states)

    if outputfiles["hfa"] != None:
        with open(outputfiles["hfa"], "w", encoding='utf-8') as fd:
            names = {}
            for (idx, s) in enumerate(dfa_states):
                names[s] = idx
            print("{", file=fd)
            print("  \"initial\": \"%s\","%names[dfa_initial_state], file=fd)
            print("  \"nodes\": [", file=fd)
            first = True
            for s in dfa_states:
                if s in dfa_error_states:
                    continue
                if first:
                    first = False
                else:
                    print(",", file=fd)
                print("    {", file=fd)
                print("      \"idx\": \"%s\","%names[s], file=fd)
                if s in dfa_final_states:
                    t = "final"
                else:
                    t = "normal"
                print("      \"type\": \"%s\""%t, file=fd)
                print("    }", end="", file=fd)
            print(file=fd)
            print("  ],", file=fd)

            print("  \"edges\": [", file=fd)
            first = True
            for (src, edges) in dfa_transitions.items():
                for (input, dst) in edges.items():
                    if dst not in dfa_error_states:
                        if first:
                            first = False
                        else:
                            print(",", file=fd)
                        print("    {", file=fd)
                        print("      \"src\": \"%s\","%names[src], file=fd)
                        print("      \"dst\": \"%s\","%names[dst], file=fd)
                        print("      \"symbol\": %s"%json.dumps(labels[input], ensure_ascii=False), file=fd)
                        print("    }", end="", file=fd)
            print(file=fd)
            print("  ]", file=fd)

            print("}", file=fd)

    if outputfiles["gv"] != None:
        with open(outputfiles["gv"], "w", encoding='utf-8') as fd:
            names = {}
            for (idx, s) in enumerate(dfa_states):
                names[s] = idx
            print("digraph {", file=fd)
            print("  rankdir = \"LR\"", file=fd)
            for s in dfa_states:
                if s in dfa_error_states:
                    continue
                if s == dfa_initial_state:
                    if s in dfa_final_states:
                        print("  s%s [label=\"initial\",style=filled,peripheries=2,fillcolor=\"#66cc33\"]"%names[s], file=fd)
                    else:
                        print("  s%s [label=\"initial\",style=filled,fillcolor=\"#66cc33\"]"%names[s], file=fd)
                else:
                    if s in dfa_final_states:
                        print("  s%s [peripheries=2,label=\"final\"]"%names[s], file=fd)
                    else:
                        print("  s%s [label=\"\"]"%names[s], file=fd)

            for (src, edges) in dfa_transitions.items():
                for (input, dst) in edges.items():
                    if dst not in dfa_error_states:
                        print("  s%s -> s%s [label=%s]"%(names[src], names[dst], json.dumps(input, ensure_ascii=False)), file=fd)
            print("}", file=fd)

    if outputfiles["png"] != None:
        if got_pydot and got_automata:
            behavior_show_diagram(dfa, path=outputfiles["png"])
        else:
            assert outputfiles["gv"] != None
            try:
                subprocess.run(["dot", "-Tpng", "-o", outputfiles["png"],
                                outputfiles["gv"] ])
            except FileNotFoundError:
                print("install graphviz (www.graphviz.org) to see output DFAs")

    if behavior != None:
        if got_automata:
            read_hfa(behavior, dfa, nfa)
        else:
            print("Can't check behavior subset because automata-lib is not available")



class ErrorToken(NamedTuple):
    line: int
    message: int
    column: int
    lexeme: str
    filename: str
    is_eof_error: bool

class HarmonyCompilerErrorCollection(Exception):
    def __init__(self, errors: List[ErrorToken]) -> None:
        super().__init__()
        self.errors = errors

class HarmonyCompilerError(Exception):
    """
    Error encountered during the compilation of a Harmony program.
    """
    def __init__(self, message: str, filename: str = None, line: int = None,
                 column: int = None, lexeme: Any = None, is_eof_error=False):
        super().__init__()
        self.message = message
        self.token = ErrorToken(
            line=line,
            message=message,
            column=column,
            lexeme=str(lexeme),
            filename=filename,
            is_eof_error=is_eof_error
        )

def bag_add(bag, item):
    cnt = bag.get(item)
    if cnt == None:
        bag[item] = 1
    else:
        bag[item] = cnt + 1

def bag_remove(bag, item):
    cnt = bag[item]
    assert cnt > 0
    if cnt == 1:
        del bag[item]
    else:
        bag[item] = cnt - 1

def doImport(scope, code, module):
    (lexeme, file, line, column) = module
    # assert lexeme not in scope.names        # TODO
    if lexeme not in imported:
        # TODO.  Only do the following if the modules have variables?
        code.append(PushOp((novalue, file, line, column)))
        code.append(StoreOp(module, module, []))

        # module name replacement with -m flag
        modname = modules[lexeme] if lexeme in modules \
                            else lexeme

        # create a new scope
        scope2 = Scope(None)
        scope2.prefix = [lexeme]
        scope2.labels = scope.labels

        found = False
        install_path = os.path.dirname(os.path.realpath(__file__))
        for dir in [ os.path.dirname(namestack[-1]), install_path + "/modules", "." ]:
            filename = dir + "/" + modname + ".hny"
            if os.path.exists(filename):
                with open(filename, encoding='utf-8') as f:
                    load(f, filename, scope2, code)
                found = True
                break
        if not found:
            raise HarmonyCompilerError(
                filename=file,
                lexeme=modname,
                message="Can't import module %s from %s" % (modname, namestack),
                line=line,
                column=column
            )
        imported[lexeme] = scope2

    scope.names[lexeme] = ("module", imported[lexeme])

def load_string(all, filename, scope, code):
    files[filename] = all.split("\n")
    tokens = lexer(all, filename)
    if tokens == []:
        raise HarmonyCompilerError(
            message="Empty file: %s" % str(filename),
            filename=filename,
            is_eof_error=True
        )

    try:
        (ast, rem) = StatListRule(-1, False).parse(tokens)
    except IndexError:
        # best guess...
        (lexeme, file, line, column) = tokens[-1]
        raise HarmonyCompilerError(
            filename=file,
            line=line,
            column=column,
            lexeme=lexeme,
            message="Parsing %s hit EOF" % str(filename),
            is_eof_error=True
        )

    if rem != []:
        (lexeme, file, line, column) = rem[0]
        raise HarmonyCompilerError(
            filename=file,
            line=line,
            column=column,
            lexeme=lexeme,
            message="Parsing: unexpected tokens remaining at end of program: %s" % str(rem[0]),
        )
    for mod in ast.getImports():
        doImport(scope, code, mod)

    # method names and label names get a temporary value
    # they are filled in with their actual values after compilation
    # TODO.  Look for duplicates?
    for ((lexeme, file, line, column), lb) in ast.getLabels():
        scope.names[lexeme] = ("constant", (lb, file, line, column))

    ast.compile(scope, code)

def load(f, filename, scope, code):
    if filename in files:
        return
    namestack.append(filename)
    all = ""
    for line in f:
        all += line
    load_string(all, filename, scope, code)
    namestack.pop()

def islower(c):
    return c in "abcdefghijklmnopqrstuvwxyz"

def isupper(c):
    return c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def isletter(c):
    return islower(c) or isupper(c)

def isnumeral(c):
    return c in "0123456789"

def isalnum(c):
    return isletter(c) or isnumeral(c)

def isnamechar(c):
    return isalnum(c) or c == "_"

def isprint(c):
    return isinstance(c, str) and len(c) == 1 and (
        isalnum(c) or c in " ~!@#$%^&*()-_=+[{]}\\|;:\",<.>/?")

def isnumber(s):
    return all(isnumeral(c) for c in s)

def isreserved(s):
    return s in {
        "all",
        "and",
        "any",
        "as",
        "assert",
        "atLabel",
        "atomic",
        "atomically",
        "await",
        # "call",
        "choose",
        "const",
        "contexts",
        "countLabel",
        "def",
        "del",
        "elif",
        "else",
        "end",
        "eternal",
        "except",
        "exists",
        "False",
        # "fun",
        "for",
        "from",
        "get_context",
        "go",
        "hash",
        "if",
        "import",
        "in",
        "inf",
        "invariant",
        "keys",
        "lambda",
        "len",
        "let",
        "max",
        "min",
        "None",
        "not",
        "or",
        "pass",
        "possibly",
        "print",
        "select",
        "sequential",
        "setintlevel",
        "spawn",
        "stop",
        "str",
        "trap",
        "try",
        "True",
        "when",
        "where",
        "while"
        "with"
    }

def isname(s):
    return (not isreserved(s)) and (isletter(s[0]) or s[0] == "_") and \
                    all(isnamechar(c) for c in s)

def isunaryop(s):
    return s in { "!", "-", "~", "abs", "all", "any", "atLabel", "choose",
        "contexts", "countLabel", "get_context", "min", "max", "not",
        "keys", "hash", "len", "str"
    }

def isxbinop(s):
    return s in {
        "and", "or", "=>", "&", "|", "^", "-", "+", "*", "/", "//", "%", "mod",
        "**", "<<", ">>"
    }

def iscmpop(s):
    return s in { "==", "!=", "<", "<=", ">", ">=" }

assignops = {
    "and=", "or=", "=>=", "&=", "|=", "^=", "-=", "+=", "*=", "/=", "//=",
    "%=", "mod=", "**=", "<<=", ">>="
}

def isbinaryop(s):
    return isxbinop(s) or iscmpop(s) or s == "in"

tokens = { "{", "==", "!=", "<=", ">=", "=>",
                        "//", "**", "<<", ">>", "..", "->" } | assignops

def lexer(s, file):
    result = []
    line = 1
    column = 1
    cont = 1
    s = s.replace('\\r', '')        # MS-DOS...
    indentChars = set()
    indent = True
    while s != "":
        # see if it's a blank
        if s[0] in { " ", "\t" }:
            if indent:
                indentChars.add(s[0])
            s = s[1:]
            column += 1
            continue

        # backslash at end of line: glue on the next line
        if s[0] == "\\":
            if len(s) == 1:
                break
            if s[1] == "\n":
                s = s[2:]
                column += 2
                cont += 1
                continue

        if s[0] == "\n":
            s = s[1:]
            line += cont
            cont = 1
            column = 1
            indent = True
            continue

        indent = False

        # skip over line comments
        if s.startswith("#"):
            s = s[1:]
            while len(s) > 0 and s[0] != '\n':
                s = s[1:]
            continue

        # skip over nested comments
        if s.startswith("(*"):
            count = 1
            s = s[2:]
            column += 2
            while count != 0 and s != "":
                if s.startswith("(*"):
                    count += 1
                    s = s[2:]
                    column += 2
                elif s.startswith("*)"):
                    count -= 1
                    s = s[2:]
                    column += 2
                elif s[0] == "\n":
                    s = s[1:]
                    line += cont
                    cont = 1
                    column = 1
                else:
                    s = s[1:]
                    column += 1
            continue

        # see if it's a multi-character token.  Match with the longest one
        found = ""
        for t in tokens:
            if s.startswith(t) and len(t) > len(found):
                found = t
        if found != "":
            result += [ (found, file, line, column) ]
            s = s[len(found):]
            column += len(found)
            continue

        # see if a sequence of letters and numbers
        if isnamechar(s[0]):
            i = 0
            while i < len(s) and isnamechar(s[i]):
                i += 1
            result += [ (s[:i], file, line, column) ]
            s = s[i:]
            column += i
            continue

        # string
        if s[0] == '"' or s[0] == "'":
            start_col = column
            if s.startswith('"""'):
                term = '"""'
            elif s.startswith("'''"):
                term = "'''"
            elif s[0] == '"':
                term = '"'
            else:
                assert s[0] == "'", s[0]
                term = "'"
            column += len(term)
            s = s[len(term):]
            str = '"'
            while s != "" and not s.startswith(term):
                if s[0] == '\\':
                    s = s[1:]
                    if s == "":
                        break
                    column += 1
                    if s[0] == 'a':
                        str += '\a'; column += 1; s = s[1:]
                    elif s[0] == 'b':
                        str += '\b'; column += 1; s = s[1:]
                    elif s[0] == 'f':
                        str += '\f'; column += 1; s = s[1:]
                    elif s[0] == 'n':
                        str += '\n'; column += 1; s = s[1:]
                    elif s[0] == 'r':
                        str += '\r'; column += 1; s = s[1:]
                    elif s[0] == 't':
                        str += '\t'; column += 1; s = s[1:]
                    elif s[0] == 'v':
                        str += '\v'; column += 1; s = s[1:]
                    elif s[0] in "01234567":
                        total = 0
                        for i in range(3):
                            if s[0] not in "01234567":
                                break
                            total *= 8
                            total += ord(s[0]) - ord("0")
                            column += 1
                            s = s[1:]
                        str += chr(total)
                    elif s[0] in { 'x', "X" }:
                        column += 1
                        s = s[1:]
                        total = 0
                        while s != "" and s[0] in "0123456789abcdefABCDEF":
                            total *= 16;
                            if s[0] in "0123456789":
                                total += ord(s[0]) - ord("0")
                            elif s[0] in "abcdef":
                                total += 10 + (ord(s[0]) - ord("a"))
                            else:
                                assert s[0] in "ABCDEF", s[0]
                                total += 10 + (ord(s[0]) - ord("A"))
                            column += 1
                            s = s[1:]
                        str += chr(total)
                    else:
                        str += s[0]
                        if s[0] == '\n':
                            line += cont
                            cont = 1
                        column += 1
                        s = s[1:]
                else:
                    str += s[0]
                    if s[0] == '\n':
                        line += cont
                        cont = 1
                    column += 1
                    s = s[1:]
            result += [ (str, file, line, start_col) ]
            column += len(term)
            s = s[len(term):]
            continue

        # everything else is a single character token
        result += [ (s[0], file, line, column) ]
        s = s[1:]
        column += 1

    if len(indentChars) > 1:
        print("WARNING: do not mix tabs in spaces for indentation")
        print("It is likely to lead to incorrect parsing and code generation")

    return result

def tlaValue(lexeme):
    if isinstance(lexeme, bool):
        return 'HBool(%s)'%("TRUE" if lexeme else "FALSE")
    if isinstance(lexeme, int):
        return 'HInt(%d)'%lexeme
    if isinstance(lexeme, str):
        return 'HStr("%s")'%lexeme
    return lexeme.tlaval()

def strValue(v):
    if isinstance(v, Value) or isinstance(v, bool) or isinstance(v, int) or isinstance(v, float):
        return str(v)
    if isinstance(v, str):
        return '"%s"'%v
    assert False, v

def jsonValue(v):
    if isinstance(v, Value):
        return v.jdump()
    if isinstance(v, bool):
        return '{ "type": "bool", "value": "%s" }'%str(v)
    if isinstance(v, int) or isinstance(v, float):
        return '{ "type": "int", "value": %s }'%str(v)
    if isinstance(v, str):
        return '{ "type": "atom", "value": %s }'%json.dumps(v, ensure_ascii=False)
    assert False, v

def strVars(v):
    assert isinstance(v, DictValue)
    result = ""
    for (var, val) in v.d.items():
        if result != "":
            result += ", "
        result += strValue(var)[1:] + "=" + strValue(val)
    return "{" + result + "}"

def keyValue(v):
    if isinstance(v, bool):
        return (0, v)
    if isinstance(v, int) or isinstance(v, float):
        return (1, v)
    if isinstance(v, str):
        return (2, v)
    assert isinstance(v, Value), v
    return v.key()

def substValue(v, map):
    return v.substitute(map) if isinstance(v, Value) else v

class Value:
    def __str__(self):
        return self.__repr__()

    def jdump(self):
        assert False

    def substitute(self, map):
        assert False, self

class PcValue(Value):
    def __init__(self, pc):
        self.pc = pc

    def __repr__(self):
        return "PC(" + str(self.pc) + ")"

    def tlaval(self):
        return 'HPc(%d)'%self.pc

    def __hash__(self):
        return self.pc.__hash__()

    def __eq__(self, other):
        return isinstance(other, PcValue) and other.pc == self.pc

    def key(self):
        return (3, self.pc)

    def jdump(self):
        return '{ "type": "pc", "value": "%d" }'%self.pc

# This is a substitute for PCValues used before values are assigned to labels
# TODO.  Get rid of all but id
class LabelValue(Value):
    def __init__(self, module, label):
        global labelid
        self.id = labelid
        labelid += 1
        self.module = module
        self.label = label

    def __repr__(self):
        if self.module == None:
            return "LABEL(" + str(self.id) + ", " + self.label + ")"
        else:
            return "LABEL(" + self.module + ":" + self.label + ")"

    def __hash__(self):
        return self.id

    def __eq__(self, other):
        return isinstance(other, LabelValue) and other.id == self.id

    def key(self):
        return (100, self.id)

    def jdump(self):
        assert False

    def substitute(self, map):
        return map[self]

class DictValue(Value):
    def __init__(self, d):
        self.d = d

    def __repr__(self):
        if len(self.d) == 0:
            return "()"
        result = ""
        if set(self.d.keys()) == set(range(len(self.d))):
            for k in range(len(self.d)):
                if result != "":
                    result += ", ";
                result += strValue(self.d[k])
            return "[" + result + "]"
        keys = sorted(self.d.keys(), key=keyValue)
        for k in keys:
            if result != "":
                result += ", ";
            result += strValue(k) + ":" + strValue(self.d[k])
        return "{ " + result + " }"

    def tlaval(self):
        global tlavarcnt

        tlavar = "x%d"%tlavarcnt
        tlavarcnt += 1
        if len(self.d) == 0:
            return 'EmptyDict'
        s = "[ %s \\in {"%tlavar + ",".join({ tlaValue(k) for k in self.d.keys() }) + "} |-> "
        # special case: all values are the same
        vals = list(self.d.values())
        if vals.count(vals[0]) == len(vals):
            s += tlaValue(vals[0]) + " ]"
            return 'HDict(%s)'%s

        # not all values are the same
        first = True
        for k,v in self.d.items():
            if first:
                s += "CASE "
                first = False
            else:
                s += " [] "
            s += "%s = "%tlavar + tlaValue(k) + " -> " + tlaValue(v)
        s += " [] OTHER -> FALSE ]"
        return 'HDict(%s)'%s

    def jdump(self):
        result = ""
        keys = sorted(self.d.keys(), key=keyValue)
        for k in keys:
            if result != "":
                result += ", ";
            result += '{ "key": %s, "value": %s }'%(jsonValue(k), jsonValue(self.d[k]))
        return '{ "type": "dict", "value": [%s] }'%result

    def __hash__(self):
        hash = 0
        for x in self.d.items():
            hash ^= x.__hash__()
        return hash

    def __eq__(self, other):
        if not isinstance(other, DictValue):
            return False
        if len(self.d.keys()) != len(other.d.keys()):   # for efficiency
            return False
        return self.d == other.d

    def __len__(self):
        return len(self.d.keys())

    # Dictionary ordering generalizes lexicographical ordering when the dictionary
    # represents a list or tuple
    def key(self):
        return (5, [ (keyValue(v), keyValue(self.d[v]))
                        for v in sorted(self.d.keys(), key=keyValue)])

    def substitute(self, map):
        return DictValue({ substValue(k, map): substValue(v, map)
                            for (k, v) in self.d.items() })

# TODO.  Is there a better way than making this global?
novalue = DictValue({})

class SetValue(Value):
    def __init__(self, s):
        self.s = s

    def __repr__(self):
        if len(self.s) == 0:
            return "{}"
        result = ""
        vals = sorted(self.s, key=keyValue)
        for v in vals:
            if result != "":
                result += ", ";
            result += strValue(v)
        return "{ " + result + " }"

    def tlaval(self):
        s = "{" + ",".join(tlaValue(x) for x in self.s) + "}"
        return 'HSet(%s)'%s

    def jdump(self):
        result = ""
        vals = sorted(self.s, key=keyValue)
        for v in vals:
            if result != "":
                result += ", ";
            result += jsonValue(v)
        return '{ "type": "set", "value": [%s] }'%result

    def __hash__(self):
        return frozenset(self.s).__hash__()

    def __eq__(self, other):
        if not isinstance(other, SetValue):
            return False
        return self.s == other.s

    def key(self):
        return (6, [keyValue(v) for v in sorted(self.s, key=keyValue)])

    def substitute(self, map):
        return SetValue({ substValue(v, map) for v in self.s })

class AddressValue(Value):
    def __init__(self, indexes):
        self.indexes = indexes

    def __repr__(self):
        if len(self.indexes) == 0:
            return "None"
        result = "?" + self.indexes[0]
        for index in self.indexes[1:]:
            if isinstance(index, str):
                result = result + strValue(index)
            else:
                result += "[" + strValue(index) + "]"
        return result

    def tlaval(self):
        s = "<<" + ",".join(tlaValue(x) for x in self.indexes) + ">>"
        return 'HAddress(%s)'%s

    def jdump(self):
        result = ""
        for index in self.indexes:
            if result != "":
                result += ", "
            result = result + jsonValue(index)
        return '{ "type": "address", "value": [%s] }'%result

    def __hash__(self):
        hash = 0
        for x in self.indexes:
            hash ^= x.__hash__()
        return hash

    def __eq__(self, other):
        if not isinstance(other, AddressValue):
            return False
        return self.indexes == other.indexes

    def key(self):
        return (7, self.indexes)

    def substitute(self, map):
        return AddressValue([ substValue(v, map) for v in self.indexes ])

class Op:
    def define(self):   # set of local variables updated by this op
        return set()

    def use(self):      # set of local variables used by this op
        return set()

    def jdump(self):
        return '{ "op": "XXX %s" }'%str(self)

    def tladump(self):
        return 'Skip(self, "%s")'%self

    def explain(self):
        return "no explanation yet"

    def sametype(x, y):
        return type(x) == type(y)

    def convert(self, x):
        if isinstance(x, tuple):
            return x[0]
        else:
            assert isinstance(x, list)
            result = "";
            for v in x:
                if result != "":
                    result += ", "
                result += self.convert(v)
            return "(" + result + ")"

    def tlaconvert(self, x):
        if isinstance(x, tuple):
            return 'VName("%s")'%x[0]
        else:
            assert isinstance(x, list)
            result = 'VList(<< '
            result += ",".join([self.tlaconvert(v) for v in x])
            return result + " >>)"

    # Return the set of local variables in x
    # TODO.  Use reduce()
    def lvars(self, x):
        if isinstance(x, tuple):
            return { x[0] }
        else:
            assert isinstance(x, list)
            result = set();
            for v in x:
                result |= self.lvars(v)
            return result

    def store(self, context, var, val):
        if isinstance(var, tuple):
            (lexeme, file, line, column) = var
            context.set([lexeme], val)
        else:
            assert isinstance(var, list)
            if not isinstance(val, DictValue):
                context.failure = "Error: pc = %d: tried to assign %s to %s"%(
                    context.pc, val, self.convert(var))
            elif len(var) != len(val.d):
                context.failure = "Error: pc = %d: cannot assign %s to %s"%(
                    context.pc, val, self.convert(var))
            else:
                for i in range(len(var)):
                    self.store(context, var[i], val.d[i])

    def load(self, context, var):
        if isinstance(var, tuple):
            (lexeme, file, line, column) = var
            return context.get(lexeme)
        else:
            assert isinstance(var, list)
            d = { i:self.load(context, var[i]) for i in range(len(var)) }
            return DictValue(d)

    def substitute(self, map):
        pass

class SetIntLevelOp(Op):
    def __repr__(self):
        return "SetIntLevel"

    def jdump(self):
        return '{ "op": "SetIntLevel" }'

    def tladump(self):
        return 'OpSetIntLevel(self)'

    def explain(self):
        return "pops new boolean interrupt level and pushes old one"

    def eval(self, state, context):
        before = context.interruptLevel
        v = context.pop()
        assert isinstance(v, bool), v
        context.interruptLevel = v
        context.push(before)
        context.pc += 1

# Splits a non-empty set or dict in its minimum element and its remainder
class CutOp(Op):
    def __init__(self, s, value, key):
        self.s = s
        self.value = value
        self.key = key

    def __repr__(self):
        if self.key == None:
            return "Cut(" + str(self.s[0]) + ", " + self.convert(self.value) + ")"
        else:
            return "Cut(" + str(self.s[0]) + ", " + self.convert(self.key) + ", " + self.convert(self.value) + ")"

    def define(self):
        if self.key == None:
            return self.lvars(self.value)
        else:
            return self.lvars(self.value) | self.lvars(self.key)

    def jdump(self):
        if self.key == None:
            return '{ "op": "Cut", "set": "%s", "value": "%s" }'%(self.s[0], self.convert(self.value))
        else:
            return '{ "op": "Cut", "set": "%s", "key": "%s", "value": "%s" }'%(self.s[0], self.convert(self.key), self.convert(self.value))

    def tladump(self):
        if self.key == None:
            return 'OpCut(self, "%s", %s)'%(self.s[0],
                                        self.tlaconvert(self.value))
        else:
            return 'OpCut3(self, "%s", %s, %s)'%(self.s[0],
                        self.tlaconvert(self.value), self.tlaconvert(self.key))

    def explain(self):
        if self.key == None:
            return "remove smallest element from %s and assign to %s"%(self.s[0], self.convert(self.value))
        else:
            return "remove smallest element from %s and assign to %s:%s"%(self.s[0], self.convert(self.key), self.convert(self.value))

    def eval(self, state, context):
        key = self.load(context, self.s)
        if isinstance(key, DictValue):
            if key.d == {}:
                context.failure = "pc = " + str(context.pc) + \
                    ": Error: expected non-empty dict value"
            else:
                select = min(key.d.keys(), key=keyValue)
                self.store(context, self.key, key.d[select])
                copy = key.d.copy()
                del copy[select]
                self.store(context, self.s, DictValue(copy))
                context.pc += 1
        else:
            if not isinstance(key, SetValue):
                context.failure = "pc = " + str(context.pc) + \
                    ": Error: expected set value, got " + str(key)
            elif key.s == set():
                context.failure = "pc = " + str(context.pc) + \
                    ": Error: expected non-empty set value"
            else:
                lst = sorted(key.s, key=keyValue)
                self.store(context, self.key, lst[0])
                self.store(context, self.s, SetValue(set(lst[1:])))
                context.pc += 1

# Splits a tuple into its elements
class SplitOp(Op):
    def __init__(self, n):
        self.n = n

    def __repr__(self):
        return "Split %d"%self.n

    def jdump(self):
        return '{ "op": "Split", "count": "%d" }'%self.n

    def tladump(self):
        return 'OpSplit(self, %d)'%self.n

    def explain(self):
        return "splits a tuple value into its elements"

    def eval(self, state, context):
        v = context.pop()
        assert isinstance(v, DictValue), v
        assert len(v.d) == self.n, (self.n, len(v.d))
        for i in range(len(v.d)):
            context.push(v.d[i])
        context.pc += 1

# Move an item in the stack to the top
class MoveOp(Op):
    def __init__(self, offset):
        self.offset = offset

    def __repr__(self):
        return "Move %d"%self.offset

    def jdump(self):
        return '{ "op": "Move", "offset": "%d" }'%self.offset

    def tladump(self):
        return 'OpMove(self, %d)'%self.offset

    def explain(self):
        return "move stack element to top"

    def eval(self, state, context):
        v = context.stack.pop(len(context.stack) - self.offset)
        context.push(v)
        context.pc += 1

class DupOp(Op):
    def __repr__(self):
        return "Dup"

    def jdump(self):
        return '{ "op": "Dup" }'

    def tladump(self):
        return 'OpDup(self)'

    def explain(self):
        return "push a copy of the top value on the stack"

    def eval(self, state, context):
        v = context.pop()
        context.push(v)
        context.push(v)
        context.pc += 1

class GoOp(Op):
    def __repr__(self):
        return "Go"

    def jdump(self):
        return '{ "op": "Go" }'

    def tladump(self):
        return 'OpGo(self)'

    def explain(self):
        return "pops a context and a value, restores the corresponding thread, and pushes the value on its stack"

    def eval(self, state, context):
        ctx = context.pop()
        if not isinstance(ctx, ContextValue):
            context.failure = "pc = " + str(context.pc) + \
                ": Error: expected context value, got " + str(ctx)
        else:
            if ctx in state.stopbag:
                cnt = state.stopbag[ctx]
                assert cnt > 0
                if cnt == 1:
                    del state.stopbag[ctx]
                else:
                    state.stopbag[ctx] = cnt - 1
            result = context.pop();
            copy = ctx.copy()
            copy.push(result)
            copy.stopped = False
            bag_add(state.ctxbag, copy)
            context.pc += 1

class LoadVarOp(Op):
    def __init__(self, v, lvar=None):
        self.v = v
        self.lvar = lvar        # name of local var if v == None

    def __repr__(self):
        if self.v == None:
            return "LoadVar [%s]"%self.lvar
        else:
            return "LoadVar " + self.convert(self.v)

    def define(self):
        return set()

    def use(self):
        if self.v == None:
            return { self.lvar }
        return self.lvars(self.v)

    def jdump(self):
        if self.v == None:
            return '{ "op": "LoadVar" }'
        else:
            return '{ "op": "LoadVar", "value": "%s" }'%self.convert(self.v)

    def tladump(self):
        if self.v == None:
            return 'OpLoadVarInd(self)'
        else:
            return 'OpLoadVar(self, %s)'%self.tlaconvert(self.v)

    def explain(self):
        if self.v == None:
            return "pop the address of a method variable and push the value of that variable"
        else:
            return "push the value of " + self.convert(self.v)

    def eval(self, state, context):
        if self.v == None:
            av = context.pop()
            assert isinstance(av, AddressValue)
            context.push(context.iget(av.indexes))
        else:
            context.push(self.load(context, self.v))
        context.pc += 1

class IncVarOp(Op):
    def __init__(self, v):
        self.v = v

    def __repr__(self):
        return "IncVar " + self.convert(self.v)

    def jdump(self):
        return '{ "op": "IncVar", "value": "%s" }'%self.convert(self.v)

    def tladump(self):
        return 'OpIncVar(self, %s)'%self.tlaconvert(self.v)

    def explain(self):
        return "increment the value of " + self.convert(self.v)

    def eval(self, state, context):
        v = self.load(context, self.v)
        self.store(context, self.v, v + 1)
        context.pc += 1

class PushOp(Op):
    def __init__(self, constant):
        self.constant = constant

    def __repr__(self):
        (lexeme, file, line, column) = self.constant
        return "Push %s"%strValue(lexeme)

    def jdump(self):
        (lexeme, file, line, column) = self.constant
        return '{ "op": "Push", "value": %s }'%jsonValue(lexeme)

    def tladump(self):
        (lexeme, file, line, column) = self.constant
        v = tlaValue(lexeme)
        return 'OpPush(self, %s)'%v

    def explain(self):
        return "push constant " + strValue(self.constant[0])

    def eval(self, state, context):
        (lexeme, file, line, column) = self.constant
        context.push(lexeme)
        context.pc += 1

    def substitute(self, map):
        (lexeme, file, line, column) = self.constant
        if isinstance(lexeme, Value):
            self.constant = (lexeme.substitute(map), file, line, column)

class LoadOp(Op):
    def __init__(self, name, token, prefix):
        self.name = name
        self.token = token
        self.prefix = prefix

    def __repr__(self):
        if self.name == None:
            return "Load"
        else:
            (lexeme, file, line, column) = self.name
            return "Load " + ".".join(self.prefix + [lexeme])

    def jdump(self):
        if self.name == None:
            return '{ "op": "Load" }'
        else:
            (lexeme, file, line, column) = self.name
            result = ""
            for n in self.prefix + [lexeme]:
                if result != "":
                    result += ", "
                result += jsonValue(n)
            return '{ "op": "Load", "value": [%s] }'%result

    def tladump(self):
        if self.name == None:
            return "OpLoadInd(self)"
        else:
            (lexeme, file, line, column) = self.name
            result = ",".join([tlaValue(x) for x in self.prefix + [lexeme]])
            return 'OpLoad(self, <<%s>>)'%result

    def explain(self):
        if self.name == None:
            return "pop an address and push the value at the address"
        else:
            return "push value of shared variable " + self.name[0]

    def eval(self, state, context):
        if self.name == None:
            av = context.pop()
            if not isinstance(av, AddressValue):
                context.failure = "Error: not an address " + \
                                    str(self.token) + " -> " + str(av)
                return
            context.push(state.iget(av.indexes))
        else:
            (lexeme, file, line, column) = self.name
            # TODO
            if False and lexeme not in state.vars.d:
                context.failure = "Error: no variable " + str(self.token)
                return
            context.push(state.iget(self.prefix + [lexeme]))
        context.pc += 1

class StoreOp(Op):
    def __init__(self, name, token, prefix):
        self.name = name
        self.token = token  # for error reporting
        self.prefix = prefix

    def __repr__(self):
        if self.name == None:
            return "Store"
        else:
            (lexeme, file, line, column) = self.name
            return "Store " + ".".join(self.prefix + [lexeme])

    def jdump(self):
        if self.name == None:
            return '{ "op": "Store" }'
        else:
            (lexeme, file, line, column) = self.name
            result = ""
            for n in self.prefix + [lexeme]:
                if result != "":
                    result += ", "
                result += jsonValue(n)
            return '{ "op": "Store", "value": [%s] }'%result

    def tladump(self):
        if self.name == None:
            return "OpStoreInd(self)"
        else:
            (lexeme, file, line, column) = self.name
            result = ",".join([tlaValue(x) for x in self.prefix + [lexeme]])
            return 'OpStore(self, <<%s>>)'%result

    def explain(self):
        if self.name == None:
            return "pop a value and an address and store the value at the address"
        else:
            return "pop a value and store it in shared variable " + self.name[0]

    def eval(self, state, context):
        if context.readonly > 0:
            context.failure = "Error: no update allowed in assert " + str(self.token)
            return
        v = context.pop()
        if self.name == None:
            av = context.pop()
            if not isinstance(av, AddressValue):
                context.failure = "Error: not an address " + \
                                    str(self.token) + " -> " + str(av)
                return
            lv = av.indexes
            if len(lv) == 0:
                context.failure = "Error: bad address " + str(self.token)
                return
            name = lv[0]
        else:
            (lexeme, file, line, column) = self.name
            lv = self.prefix + [lexeme]
            name = lexeme

        # TODO
        if False and not state.initializing and (name not in state.vars.d):
            context.failure = "Error: using an uninitialized shared variable " \
                    + name + ": " + str(self.token)
        else:
            try:
                state.set(lv, v)
                context.pc += 1
            except AttributeError:
                context.failure = "Error: " + name + " is not a dictionary " + str(self.token)

class DelOp(Op):
    def __init__(self, name, prefix):
        self.name = name
        self.prefix = prefix

    def __repr__(self):
        if self.name != None:
            (lexeme, file, line, column) = self.name
            return "Del " + ".".join(self.prefix + [lexeme])
        else:
            return "Del"

    def jdump(self):
        if self.name == None:
            return '{ "op": "Del" }'
        else:
            (lexeme, file, line, column) = self.name
            result = ""
            for n in self.prefix + [lexeme]:
                if result != "":
                    result += ", "
                result += jsonValue(n)
            return '{ "op": "Del", "value": [%s] }'%result

    def tladump(self):
        if self.name == None:
            return "OpDelInd(self)"
        else:
            (lexeme, file, line, column) = self.name
            result = ",".join([tlaValue(x) for x in self.prefix + [lexeme]])
            return 'OpDel(self, <<%s>>)'%result

    def explain(self):
        if self.name == None:
            return "pop an address and delete the shared variable at the address"
        else:
            return "delete the shared variable " + self.name[0]

    def eval(self, state, context):
        if self.name == None:
            av = context.pop()
            if not isinstance(av, AddressValue):
                context.failure = "Error: not an address " + \
                                    str(self.token) + " -> " + str(av)
                return
            lv = av.indexes
            name = lv[0]
        else:
            (lexeme, file, line, column) = self.name
            lv = [lexeme]
            name = lexeme

        if not state.initializing and (name not in state.vars.d):
            context.failure = "Error: deleting an uninitialized shared variable " \
                    + name + ": " + str(self.token)
        else:
            state.delete(lv)
            context.pc += 1

class SaveOp(Op):
    def __repr__(self):
        return "Save"

    def jdump(self):
        return '{ "op": "Save" }'

    def tladump(self):
        return "OpSave(self)"

    def explain(self):
        return "pop a value and save context"

    def eval(self, state, context):
        assert False

class StopOp(Op):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        if self.name != None:
            (lexeme, file, line, column) = self.name
            return "Stop " + lexeme
        else:
            return "Stop"

    def jdump(self):
        if self.name != None:
            (lexeme, file, line, column) = self.name
            return '{ "op": "Stop", "value": %s }'%lexeme
        else:
            return '{ "op": "Stop" }'

    def tladump(self):
        if self.name == None:
            return "OpStopInd(self)"
        else:
            (lexeme, file, line, column) = self.name
            return "OpStop(self, %s)"%lexeme

    def explain(self):
        if self.name == None:
            return "pop an address and store context at that address"
        else:
            return "store context at " + self.name[0]

    def eval(self, state, context):
        if self.name == None:
            av = context.pop()
            if not isinstance(av, AddressValue):
                context.failure = "Error: not an address " + \
                                    str(self.name) + " -> " + str(av)
                return
            lv = av.indexes
            name = lv[0]
        else:
            (lexeme, file, line, column) = self.name
            lv = [lexeme]
            name = lexeme

        if not state.initializing and (name not in state.vars.d):
            context.failure = "Error: using an uninitialized shared variable " \
                    + name + ": " + str(self.name)
        else:
            # Update the context before saving it
            context.stopped = True
            context.pc += 1
            assert isinstance(state.code[context.pc], ContinueOp)

            # Save the context
            state.stop(lv, context)

class SequentialOp(Op):
    def __init__(self):
        pass

    def __repr__(self):
        return "Sequential"

    def jdump(self):
        return '{ "op": "Sequential" }'

    def tladump(self):
        return 'OpSequential(self)'

    def explain(self):
        return "sequential consistency for variable on top of stack"

    def eval(self, state, context):
        # TODO
        context.pop()

class ContinueOp(Op):
    def __repr__(self):
        return "Continue"

    def explain(self):
        return "a no-op, must follow a Stop operation"

    def jdump(self):
        return '{ "op": "Continue" }'

    def tladump(self):
        return 'OpContinue(self)'

    def eval(self, state, context):
        context.pc += 1

# TODO.  Address should be a 1-ary operator
class AddressOp(Op):
    def __repr__(self):
        return "Address"

    def jdump(self):
        return '{ "op": "Address" }'

    def tladump(self):
        return "OpBin(self, FunAddress)"

    def explain(self):
        return "combine the top two values on the stack into an address and push the result"

    def eval(self, state, context):
        index = context.pop()
        av = context.pop()
        assert isinstance(av, AddressValue), av
        context.push(AddressValue(av.indexes + [index]))
        context.pc += 1

class StoreVarOp(Op):
    def __init__(self, v, lvar=None):
        self.v = v
        self.lvar = lvar        # name of local var if v == None

    def __repr__(self):
        if self.v == None:
            return "StoreVar [%s]"%self.lvar
        else:
            return "StoreVar " + self.convert(self.v)

    # In case of StoreVar(x[?]), x does not get defined, only used
    def define(self):
        if self.v == None:
            return set()
        return self.lvars(self.v)

    # if v == None, only part of self.lvar is updated--the rest is used
    def use(self):
        if self.v == None:
            return { self.lvar }
        return set()

    def jdump(self):
        if self.v == None:
            return '{ "op": "StoreVar" }'
        else:
            return '{ "op": "StoreVar", "value": "%s" }'%self.convert(self.v)

    def tladump(self):
        if self.v == None:
            return 'OpStoreVarInd(self)'
        else:
            return 'OpStoreVar(self, %s)'%self.tlaconvert(self.v)

    def explain(self):
        if self.v == None:
            return "pop a value and the address of a method variable and store the value at that address"
        else:
            return "pop a value and store in " + self.convert(self.v)

    # TODO.  Check error message.  Doesn't seem right
    def eval(self, state, context):
        if self.v == None:
            value = context.pop()
            av = context.pop();
            assert isinstance(av, AddressValue)
            try:
                context.set(av.indexes, value)
                context.pc += 1
            except AttributeError:
                context.failure = "Error: " + str(av.indexes) + " not a dictionary"
        else:
            try:
                self.store(context, self.v, context.pop())
                context.pc += 1
            except AttributeError:
                context.failure = "Error: " + str(self.v) + " -- not a dictionary"

class DelVarOp(Op):
    def __init__(self, v, lvar=None):
        self.v = v
        self.lvar = lvar

    def __repr__(self):
        if self.v == None:
            return "DelVar [%s]"%self.lvar
        else:
            (lexeme, file, line, column) = self.v
            return "DelVar " + str(lexeme)

    # if v == None, self.lvar is used but not defined
    def define(self):
        if self.v == None:
            return set()
        return self.lvars(self.v)

    # if v == None, only part of self.lvar is deleted--the rest is used
    def use(self):
        if self.v == None:
            return { self.lvar }
        return set()

    def jdump(self):
        if self.v == None:
            return '{ "op": "DelVar" }'
        else:
            return '{ "op": "DelVar", "value": "%s" }'%self.convert(self.v)

    def tladump(self):
        if self.v == None:
            return 'OpDelVarInd(self)'
        else:
            return 'OpDelVar(self, %s)'%self.tlaconvert(self.v)

    def explain(self):
        if self.v == None:
            return "pop an address of a method variable and delete that variable"
        else:
            return "delete method variable " + self.v[0]

    def eval(self, state, context):
        if self.v == None:
            av = context.pop();
            assert isinstance(av, AddressValue)
            context.delete(av.indexes)
        else:
            (lexeme, file, line, column) = self.v
            context.delete([lexeme])
        context.pc += 1

class ChooseOp(Op):
    def __repr__(self):
        return "Choose"

    def jdump(self):
        return '{ "op": "Choose" }'

    def tladump(self):
        return 'OpChoose(self)'

    def explain(self):
        return "pop a set value and push one of its elements"

    def eval(self, state, context):
        v = context.pop()
        assert isinstance(v, SetValue), v
        assert len(v.s) == 1, v
        for e in v.s:
            context.push(e)
        context.pc += 1

class AssertOp(Op):
    def __init__(self, token, exprthere):
        self.token = token
        self.exprthere = exprthere

    def __repr__(self):
        return "Assert2" if self.exprthere else "Assert"

    def jdump(self):
        if self.exprthere:
            return '{ "op": "Assert2" }'
        else:
            return '{ "op": "Assert" }'

    def tladump(self):
        (lexeme, file, line, column) = self.token
        msg = '"Harmony Assertion (file=%s, line=%d) failed"'%(file, line)
        if self.exprthere:
            return 'OpAssert2(self, %s)'%msg
        else:
            return 'OpAssert(self, %s)'%msg

    def explain(self):
        if self.exprthere:
            return "pop a value and a condition and raise exception if condition is false"
        else:
            return "pop a condition and raise exception if condition is false"

    def eval(self, state, context):
        if self.exprthere:
            expr = context.pop()
        cond = context.pop()
        if not isinstance(cond, bool):
            context.failure = "Error: argument to " + str(self.token) + \
                        " must be a boolean: " + strValue(cond)
            return
        if not cond:
            (lexeme, file, line, column) = self.token
            context.failure = "Harmony Assertion (file=%s, line=%d) failed"%(file, line)
            if self.exprthere:
                context.failure += ": " + strValue(expr)
            return
        context.pc += 1

class PrintOp(Op):
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return "Print"

    def jdump(self):
        return '{ "op": "Print" }'

    def tladump(self):
        return 'OpPrint(self)'

    def explain(self):
        return "pop a value and add to print history"

    def eval(self, state, context):
        cond = context.pop()
        context.pc += 1
        assert False

class PossiblyOp(Op):
    def __init__(self, token, index):
        self.token = token
        self.index = index

    def __repr__(self):
        return "Possibly %d"%self.index

    def jdump(self):
        return '{ "op": "Possibly", "index": "%d" }'%self.index

    def explain(self):
        return "pop a condition and check"

class PopOp(Op):
    def __init__(self):
        pass

    def __repr__(self):
        return "Pop"

    def jdump(self):
        return '{ "op": "Pop" }'

    def tladump(self):
        return 'OpPop(self)'

    def explain(self):
        return "discard the top value on the stack"

    def eval(self, state, context):
        context.pop()
        context.pc += 1

class FrameOp(Op):
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __repr__(self):
        (lexeme, file, line, column) = self.name
        return "Frame " + str(lexeme) + " " + self.convert(self.args)

    def define(self):
        return self.lvars(self.args) | { "result" }

    def jdump(self):
        (lexeme, file, line, column) = self.name
        return '{ "op": "Frame", "name": "%s", "args": "%s" }'%(lexeme, self.convert(self.args))

    def tladump(self):
        (lexeme, file, line, column) = self.name
        return 'OpFrame(self, "%s", %s)'%(lexeme, self.tlaconvert(self.args))

    def explain(self):
        return "start of method " + str(self.name[0])

    def eval(self, state, context):
        arg = context.pop()
        context.push(arg)               # restore for easier debugging
        context.push(context.vars)
        context.push(context.fp)
        context.fp = len(context.stack) # points to old fp, old vars, and return address
        context.vars = DictValue({ "result": novalue })
        self.store(context, self.args, arg)
        context.pc += 1

class ReturnOp(Op):
    def __repr__(self):
        return "Return"

    def jdump(self):
        return '{ "op": "Return" }'

    def tladump(self):
        return 'OpReturn(self)'

    def use(self):
        return { "result" }

    def explain(self):
        return "restore caller method state and push result"

    def eval(self, state, context):
        if len(context.stack) == 0:
            context.phase = "end"
            return
        result = context.get("result")
        context.fp = context.pop()
        context.vars = context.pop()
        context.pop()       # argument saved for stack trace
        assert isinstance(context.vars, DictValue)
        if len(context.stack) == 0:
            context.phase = "end"
            return
        calltype = context.pop()
        if calltype == "normal":
            pc = context.pop()
            assert isinstance(pc, PcValue)
            assert pc.pc != context.pc
            context.pc = pc.pc
            context.push(result)
        elif calltype == "interrupt":
            assert context.interruptLevel
            context.interruptLevel = False
            pc = context.pop()
            assert isinstance(pc, PcValue)
            assert pc.pc != context.pc
            context.pc = pc.pc
        elif calltype == "process":
            context.phase = "end"
        else:
            assert False, calltype

class SpawnOp(Op):
    def __init__(self, eternal):
        self.eternal = eternal

    def __repr__(self):
        return "Spawn"

    def jdump(self):
        return '{ "op": "Spawn", "eternal": "%s" }'%("True" if self.eternal else "False")

    def tladump(self):
        return 'OpSpawn(self)'

    def explain(self):
        return "pop thread-local state, argument, and pc and spawn a new thread"

    def eval(self, state, context):
        if context.readonly > 0:
            context.failure = "Error: no spawn allowed in assert"
            return
        this = context.pop()
        arg = context.pop()
        method = context.pop()
        assert isinstance(method, PcValue)
        frame = state.code[method.pc]
        assert isinstance(frame, FrameOp)
        ctx = ContextValue(frame.name, method.pc, arg, this)
        ctx.push("process")
        ctx.push(arg)
        bag_add(state.ctxbag, ctx)
        context.pc += 1

class TrapOp(Op):
    def __repr__(self):
        return "Trap"

    def explain(self):
        return "pop a pc and argument and set trap"

    def jdump(self):
        return '{ "op": "Trap" }'

    def tladump(self):
        return 'OpTrap(self)'

    def eval(self, state, context):
        method = context.pop()
        assert isinstance(method, PcValue)
        arg = context.pop()
        frame = state.code[method.pc]
        assert isinstance(frame, FrameOp)
        context.trap = (method, arg)
        context.pc += 1

class AtomicIncOp(Op):
    def __init__(self, lazy):
        self.lazy = lazy

    def __repr__(self):
        return "AtomicInc(%s)"%("lazy" if self.lazy else "eager")

    def tladump(self):
        return 'OpAtomicInc(self)'

    def jdump(self):
        return '{ "op": "AtomicInc", "lazy": "%s" }'%str(self.lazy)

    def explain(self):
        return "increment atomic counter of context; thread runs uninterrupted if larger than 0"

    def eval(self, state, context):
        context.atomic += 1
        context.pc += 1

class AtomicDecOp(Op):
    def __repr__(self):
        return "AtomicDec"

    def jdump(self):
        return '{ "op": "AtomicDec" }'

    def tladump(self):
        return 'OpAtomicDec(self)'

    def explain(self):
        return "decrement atomic counter of context"

    def eval(self, state, context):
        assert context.atomic > 0
        context.atomic -= 1
        context.pc += 1

class ReadonlyIncOp(Op):
    def __repr__(self):
        return "ReadonlyInc"

    def jdump(self):
        return '{ "op": "ReadonlyInc" }'

    def explain(self):
        return "increment readonly counter of context; thread cannot mutate shared variables if > 0"

    def tladump(self):
        return 'OpReadonlyInc(self)'

    def eval(self, state, context):
        context.readonly += 1
        context.pc += 1

class ReadonlyDecOp(Op):
    def __repr__(self):
        return "ReadonlyDec"

    def jdump(self):
        return '{ "op": "ReadonlyDec" }'

    def tladump(self):
        return 'OpReadonlyDec(self)'

    def explain(self):
        return "decrement readonly counter of context"

    def eval(self, state, context):
        assert context.readonly > 0
        context.readonly -= 1
        context.pc += 1

class InvariantOp(Op):
    def __init__(self, end, token):
        self.end = end
        self.token = token

    def __repr__(self):
        return "Invariant " + str(self.end)

    def jdump(self):
        return '{ "op": "Invariant", "end": "%d" }'%self.end

    def tladump(self):
        return 'OpInvariant(self, %d)'%self.end

    def explain(self):
        return "test invariant"

    def eval(self, state, context):
        assert self.end > 0
        state.invariants |= {context.pc}
        context.pc += (self.end + 1)

    def substitute(self, map):
        if isinstance(self.end, LabelValue):
            assert isinstance(map[self.end], PcValue)
            self.end = map[self.end].pc

class JumpOp(Op):
    def __init__(self, pc):
        self.pc = pc

    def __repr__(self):
        return "Jump " + str(self.pc)

    def jdump(self):
        return '{ "op": "Jump", "pc": "%d" }'%self.pc

    def tladump(self):
        return 'OpJump(self, %d)'%self.pc

    def explain(self):
        return "set program counter to " + str(self.pc)

    def eval(self, state, context):
        assert self.pc != context.pc
        context.pc = self.pc

    def substitute(self, map):
        if isinstance(self.pc, LabelValue):
            assert isinstance(map[self.pc], PcValue)
            self.pc = map[self.pc].pc

class JumpCondOp(Op):
    def __init__(self, cond, pc):
        self.cond = cond
        self.pc = pc

    def __repr__(self):
        return "JumpCond " + str(self.cond) + " " + str(self.pc)

    def jdump(self):
        return '{ "op": "JumpCond", "pc": "%d", "cond": %s }'%(self.pc, jsonValue(self.cond))

    def tladump(self):
        return 'OpJumpCond(self, %d, %s)'%(self.pc, tlaValue(self.cond))

    def explain(self):
        return "pop a value and jump to " + str(self.pc) + \
            " if the value is " + strValue(self.cond)

    def eval(self, state, context):
        c = context.pop()
        if c == self.cond:
            assert self.pc != context.pc
            context.pc = self.pc
        else:
            context.pc += 1

    def substitute(self, map):
        if isinstance(self.pc, LabelValue):
            assert isinstance(map[self.pc], PcValue)
            self.pc = map[self.pc].pc

class NaryOp(Op):
    def __init__(self, op, n):
        self.op = op
        self.n = n

    def __repr__(self):
        (lexeme, file, line, column) = self.op
        return "%d-ary "%self.n + str(lexeme)

    def jdump(self):
        (lexeme, file, line, column) = self.op
        return '{ "op": "Nary", "arity": %d, "value": "%s" }'%(self.n, lexeme)

    def tladump(self):
        (lexeme, file, line, column) = self.op
        if lexeme == "-" and self.n == 1:
            return "OpUna(self, FunMinus)"
        if lexeme == "~" and self.n == 1:
            return "OpUna(self, FunNegate)"
        if lexeme == "not" and self.n == 1:
            return "OpUna(self, FunNot)"
        if lexeme == "str" and self.n == 1:
            return "OpUna(self, FunStr)"
        if lexeme == "len" and self.n == 1:
            return "OpUna(self, FunLen)"
        if lexeme == "min" and self.n == 1:
            return "OpUna(self, FunMin)"
        if lexeme == "max" and self.n == 1:
            return "OpUna(self, FunMax)"
        if lexeme == "abs" and self.n == 1:
            return "OpUna(self, FunAbs)"
        if lexeme == "any" and self.n == 1:
            return "OpUna(self, FunAny)"
        if lexeme == "all" and self.n == 1:
            return "OpUna(self, FunAll)"
        if lexeme == "keys" and self.n == 1:
            return "OpUna(self, FunKeys)"
        if lexeme == "IsEmpty" and self.n == 1:
            return "OpUna(self, FunIsEmpty)"
        if lexeme == "countLabel" and self.n == 1:
            return "OpUna(self, FunCountLabel)"
        if lexeme == "get_context" and self.n == 1:
            return "OpGetContext(self)"
        if lexeme == ">>" and self.n == 2:
            return "OpBin(self, FunShiftRight)"
        if lexeme == "<<" and self.n == 2:
            return "OpBin(self, FunShiftLeft)"
        if lexeme == ".." and self.n == 2:
            return "OpBin(self, FunRange)"
        if lexeme == "SetAdd" and self.n == 2:
            return "OpBin(self, FunSetAdd)"
        if lexeme == "in" and self.n == 2:
            return "OpBin(self, FunIn)"
        if lexeme == "==" and self.n == 2:
            return "OpBin(self, FunEquals)"
        if lexeme == "!=" and self.n == 2:
            return "OpBin(self, FunNotEquals)"
        if lexeme == "<" and self.n == 2:
            return "OpBin(self, FunLT)"
        if lexeme == "<=" and self.n == 2:
            return "OpBin(self, FunLE)"
        if lexeme == ">" and self.n == 2:
            return "OpBin(self, FunGT)"
        if lexeme == ">=" and self.n == 2:
            return "OpBin(self, FunGE)"
        if lexeme == "-" and self.n == 2:
            return "OpBin(self, FunSubtract)"
        if lexeme == "+":
            return "OpNary(self, FunAdd, %d)"%self.n
        if lexeme == "*":
            return "OpNary(self, FunMult, %d)"%self.n
        if lexeme == "|":
            return "OpNary(self, FunUnion, %d)"%self.n
        if lexeme == "&":
            return "OpNary(self, FunIntersect, %d)"%self.n
        if lexeme == "^":
            return "OpNary(self, FunExclusion, %d)"%self.n
        if lexeme in { "/", "//" } and self.n == 2:
            return "OpBin(self, FunDiv)"
        if lexeme in { "%", "mod" } and self.n == 2:
            return "OpBin(self, FunMod)"
        if lexeme == "**" and self.n == 2:
            return "OpBin(self, FunPower)"
        if lexeme == "DictAdd" and self.n == 3:
            return "OpDictAdd(self)"
        return 'Skip(self, "%s")'%self

    def explain(self):
        return "pop " + str(self.n) + \
            (" value" if self.n == 1 else " values") + \
            " and push the result of applying " + self.op[0]

    def atLabel(self, state, pc):
        bag = {}
        for (ctx, cnt) in state.ctxbag.items():
            if ctx.pc == pc:
                nametag = DictValue({ 0: PcValue(ctx.entry), 1: ctx.arg })
                c = bag.get(nametag)
                bag[nametag] = cnt if c == None else (c + cnt)
        return DictValue(bag)

    def countLabel(self, state, pc):
        result = 0
        for (ctx, cnt) in state.ctxbag.items():
            if ctx.pc == pc:
                result += 1
        return result

    def contexts(self, state):
        return DictValue({ **state.ctxbag, **state.termbag, **state.stopbag })

    def concat(self, d1, d2):
        result = []
        keys = sorted(d1.d.keys(), key=keyValue)
        for k in keys:
            result.append(d1.d[k])
        keys = sorted(d2.d.keys(), key=keyValue)
        for k in keys:
            result.append(d2.d[k])
        return DictValue({ i:result[i] for i in range(len(result)) })

    def checktype(self, state, context, args, chk):
        assert len(args) == self.n, (self, args)
        if not chk:
            context.failure = "Error: unexpected types in " + str(self.op) + \
                        " operands: " + str(list(reversed(args)))
            return False
        return True

    def checkdmult(self, state, context, args, d, e):
        if not self.checktype(state, context, args, type(e) == int):
            return False
        keys = set(range(len(d.d)))
        if d.d.keys() != keys:
            context.failure = "Error: one operand in " + str(self.op) + \
                        " must be a list: " + str(list(reversed(args)))
            return False
        return True

    def dmult(self, d, e):
        n = len(d.d)
        lst = { i:d.d[i % n] for i in range(e * n) }
        return DictValue(lst)

    def eval(self, state, context):
        (op, file, line, column) = self.op
        assert len(context.stack) >= self.n
        sa = context.stack[-self.n:]
        if op in { "+", "*", "&", "|", "^" }:
            assert self.n > 1
            e2 = context.pop()
            for i in range(1, self.n):
                e1 = context.pop()
                if op == "+":
                    if type(e1) == int:
                        if not self.checktype(state, context, sa, type(e2) == int):
                            return
                        e2 += e1
                    elif type(e1) == str:
                        if not self.checktype(state, context, sa, type(e2) == str):
                            return
                        e2 = e1 + e2
                    else:
                        if not self.checktype(state, context, sa, isinstance(e1, DictValue)):
                            return
                        if not self.checktype(state, context, sa, isinstance(e2, DictValue)):
                            return
                        e2 = self.concat(e1, e2)
                elif op == "*":
                    if isinstance(e1, DictValue) or isinstance(e2, DictValue):
                        if isinstance(e1, DictValue) and not self.checkdmult(state, context, sa, e1, e2):
                            return
                        if isinstance(e2, DictValue) and not self.checkdmult(state, context, sa, e2, e1):
                            return
                        e2 = self.dmult(e1, e2) if isinstance(e1, DictValue) else self.dmult(e2, e1)
                    elif isinstance(e1, str) or isinstance(e2, str):
                        if isinstance(e1, str) and not self.checktype(state, context, sa, isinstance(e2, int)):
                            return
                        if isinstance(e2, str) and not self.checktype(state, context, sa, isinstance(e1, int)):
                            return
                        e2 *= e1
                    else:
                        if not self.checktype(state, context, sa, type(e1) == int):
                            return
                        if not self.checktype(state, context, sa, type(e2) == int):
                            return
                        e2 *= e1
                elif op == "&":
                    if type(e1) == int:
                        if not self.checktype(state, context, sa, type(e2) == int):
                            return
                        e2 &= e1
                    elif type(e1) == SetValue:
                        if not self.checktype(state, context, sa, isinstance(e2, SetValue)):
                            return
                        e2 = SetValue(e1.s & e2.s)
                    else:
                        if not self.checktype(state, context, sa, isinstance(e1, DictValue)):
                            return
                        if not self.checktype(state, context, sa, isinstance(e2, DictValue)):
                            return
                        d = {}
                        for (k1, v1) in e1.d.items():
                            if k1 in e2.d:
                                v2 = e2.d[k1]
                                d[k1] = v1 if keyValue(v1) < keyValue(v2) else v2
                        e2 = DictValue(d)
                elif op == "|":
                    if type(e1) == int:
                        if not self.checktype(state, context, sa, type(e2) == int):
                            return
                        e2 |= e1
                    elif type(e1) == SetValue:
                        if not self.checktype(state, context, sa, isinstance(e2, SetValue)):
                            return
                        e2 = SetValue(e1.s | e2.s)
                    else:
                        if not self.checktype(state, context, sa, isinstance(e1, DictValue)):
                            return
                        if not self.checktype(state, context, sa, isinstance(e2, DictValue)):
                            return
                        d = {}
                        for (k1, v1) in e1.d.items():
                            if k1 in e2.d:
                                v2 = e2.d[k1]
                                d[k1] = v1 if keyValue(v1) > keyValue(v2) else v2
                            else:
                                d[k1] = v1
                        for (k2, v2) in e2.d.items():
                            if k2 not in e1.d:
                                d[k2] = v2
                        e2 = DictValue(d)
                elif op == "^": 
                    if type(e1) == int:
                        if not self.checktype(state, context, sa, type(e2) == int):
                            return
                        e2 ^= e1
                    else:
                        if not self.checktype(state, context, sa, isinstance(e1, SetValue)):
                            return
                        if not self.checktype(state, context, sa, isinstance(e2, SetValue)):
                            return
                        e2 = SetValue(e2.s.union(e1.s).difference(e2.s.intersection(e1.s)))
                else:
                    assert False, op
            context.push(e2)
        elif self.n == 1:
            e = context.pop()
            if op == "-":
                if not self.checktype(state, context, sa, type(e) == int or isinstance(e, float)):
                    return
                context.push(-e)
            elif op == "~":
                if not self.checktype(state, context, sa, type(e) == int):
                    return
                context.push(~e)
            elif op == "not":
                if not self.checktype(state, context, sa, isinstance(e, bool)):
                    return
                context.push(not e)
            elif op == "abs":
                if not self.checktype(state, context, sa, type(e) == int):
                    return
                context.push(abs(e))
            elif op == "atLabel":
                if not context.atomic:
                    context.failure = "not in atomic block: " + str(self.op)
                    return
                if not self.checktype(state, context, sa, isinstance(e, PcValue)):
                    return
                context.push(self.atLabel(state, e.pc))
            elif op == "countLabel":
                if not context.atomic:
                    context.failure = "not in atomic block: " + str(self.op)
                    return
                if not self.checktype(state, context, sa, isinstance(e, PcValue)):
                    return
                context.push(self.countLabel(state, e.pc))
            elif op == "get_context":
                # if not self.checktype(state, context, sa, isinstance(e, int)):
                #   return
                context.push(context.copy())
            elif op == "contexts":
                if not context.atomic:
                    context.failure = "not in atomic block: " + str(self.op)
                    return
                # if not self.checktype(state, context, sa, isinstance(e, str)):
                #     return
                context.push(self.contexts(state))
            elif op == "IsEmpty":
                if isinstance(e, DictValue):
                    context.push(e.d == {})
                elif self.checktype(state, context, sa, isinstance(e, SetValue)):
                    context.push(e.s == set())
            elif op == "min":
                if isinstance(e, DictValue):
                    if len(e.d) == 0:
                        context.failure = "Error: min() invoked with empty dict: " + str(self.op)
                    else:
                        context.push(min(e.d.values(), key=keyValue))
                else:
                    if not self.checktype(state, context, sa, isinstance(e, SetValue)):
                        return
                    if len(e.s) == 0:
                        context.failure = "Error: min() invoked with empty set: " + str(self.op)
                    else:
                        context.push(min(e.s, key=keyValue))
            elif op == "max":
                if isinstance(e, DictValue):
                    if len(e.d) == 0:
                        context.failure = "Error: max() invoked with empty dict: " + str(self.op)
                    else:
                        context.push(max(e.d.values(), key=keyValue))
                else:
                    if not self.checktype(state, context, sa, isinstance(e, SetValue)):
                        return
                    if len(e.s) == 0:
                        context.failure = "Error: max() invoked with empty set: " + str(self.op)
                    else:
                        context.push(max(e.s, key=keyValue))
            elif op == "len":
                if isinstance(e, SetValue):
                    context.push(len(e.s))
                elif isinstance(e, str):
                    context.push(len(e))
                else:
                    if not self.checktype(state, context, sa, isinstance(e, DictValue)):
                        return
                    context.push(len(e.d))
            elif op == "str":
                context.push(strValue(e))
            elif op == "any":
                if isinstance(e, SetValue):
                    context.push(any(e.s))
                else:
                    if not self.checktype(state, context, sa, isinstance(e, DictValue)):
                        return
                    context.push(any(e.d.values()))
            elif op == "all":
                if isinstance(e, SetValue):
                    context.push(all(e.s))
                else:
                    if not self.checktype(state, context, sa, isinstance(e, DictValue)):
                        return
                    context.push(all(e.d.values()))
            elif op == "keys":
                if not self.checktype(state, context, sa, isinstance(e, DictValue)):
                    return
                context.push(SetValue(set(e.d.keys())))
            elif op == "hash":
                context.push((e,).__hash__())
            else:
                assert False, self
        elif self.n == 2:
            e2 = context.pop()
            e1 = context.pop()
            if op == "==":
                # if not self.checktype(state, context, sa, type(e1) == type(e2)):
                #     return
                context.push(e1 == e2)
            elif op == "!=":
                # if not self.checktype(state, context, sa, type(e1) == type(e2)):
                #     return
                context.push(e1 != e2)
            elif op == "<":
                context.push(keyValue(e1) < keyValue(e2))
            elif op == "<=":
                context.push(keyValue(e1) <= keyValue(e2))
            elif op == ">":
                context.push(keyValue(e1) > keyValue(e2))
            elif op == ">=":
                context.push(keyValue(e1) >= keyValue(e2))
            elif op == "-":
                if type(e1) == int or isinstance(e1, float):
                    if not self.checktype(state, context, sa, type(e2) == int or isinstance(e2, float)):
                        return
                    context.push(e1 - e2)
                else:
                    if not self.checktype(state, context, sa, isinstance(e1, SetValue)):
                        return
                    if not self.checktype(state, context, sa, isinstance(e2, SetValue)):
                        return
                    context.push(SetValue(e1.s.difference(e2.s)))
            elif op in { "/", "//" }:
                if not self.checktype(state, context, sa, type(e1) == int or isinstance(e1, float)):
                    return
                if not self.checktype(state, context, sa, type(e2) == int or isinstance(e2, float)):
                    return
                if type(e1) == int and (e2 == math.inf or e2 == -math.inf):
                    context.push(0)
                else:
                    context.push(e1 // e2)
            elif op in { "%", "mod" }:
                if not self.checktype(state, context, sa, type(e1) == int):
                    return
                if not self.checktype(state, context, sa, type(e2) == int):
                    return
                context.push(e1 % e2)
            elif op == "**":
                if not self.checktype(state, context, sa, type(e1) == int):
                    return
                if not self.checktype(state, context, sa, type(e2) == int):
                    return
                context.push(e1 ** e2)
            elif op == "<<":
                if not self.checktype(state, context, sa, type(e1) == int):
                    return
                if not self.checktype(state, context, sa, type(e2) == int):
                    return
                context.push(e1 << e2)
            elif op == ">>":
                if not self.checktype(state, context, sa, type(e1) == int):
                    return
                if not self.checktype(state, context, sa, type(e2) == int):
                    return
                context.push(e1 >> e2)
            elif op == "..":
                if not self.checktype(state, context, sa, type(e1) == int):
                    return
                if not self.checktype(state, context, sa, type(e2) == int):
                    return
                context.push(SetValue(set(range(e1, e2+1))))
            elif op == "in":
                if isinstance(e2, SetValue):
                    context.push(e1 in e2.s)
                elif isinstance(e2, str):
                    if not self.checktype(state, context, sa, isinstance(e1, str)):
                        return
                    context.push(e1 in e2)
                elif not self.checktype(state, context, sa, isinstance(e2, DictValue)):
                    return
                else:
                    context.push(e1 in e2.d.values())
            elif op == "SetAdd":
                assert isinstance(e1, SetValue)
                context.push(SetValue(e1.s | {e2}))
            elif op == "BagAdd":
                assert isinstance(e1, DictValue)
                d = e1.d.copy()
                if e2 in d:
                    assert isinstance(d[e2], int)
                    d[e2] += 1
                else:
                    d[e2] = 1
                context.push(DictValue(d))
            else:
                assert False, self
        elif self.n == 3:
            e3 = context.pop()
            e2 = context.pop()
            e1 = context.pop()
            if op == "DictAdd":
                assert isinstance(e1, DictValue)
                d = e1.d.copy()
                if e2 in d:
                    if keyValue(d[e2]) >= keyValue(e3):
                        context.push(e1)
                    else:
                        d[e2] = e3
                        context.push(DictValue(d))
                else:
                    d[e2] = e3
                    context.push(DictValue(d))
            else:
                assert False, self
        else:
            assert False, self
        context.pc += 1

class ApplyOp(Op):
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return "Apply"

    def jdump(self):
        return '{ "op": "Apply" }'

    def tladump(self):
        return 'OpApply(self)'

    def explain(self):
        return "pop a pc or dictionary f and an index i and push f(i)"

    def eval(self, state, context):
        e = context.pop()
        method = context.pop()
        if isinstance(method, DictValue):
            try:
                context.push(method.d[e])
            except KeyError:
                context.failure = "Error: no entry " + str(e) + " in " + \
                        str(self.token) + " = " + str(method)
                return
            context.pc += 1
        elif isinstance(method, ContextValue):
            if e == "this":
                context.push(method.this)
            elif e == "name":
                context.push(method.name)
            elif e == "entry":
                context.push(method.entry)
            elif e == "arg":
                context.push(method.arg)
            elif e == "mode":
                if method.failure != None:
                    context.push("failed")
                elif method.phase == "end":
                    context.push("terminated")
                elif method.stopped:
                    context.push("stopped")
                else:
                    context.push("normal")
            context.pc += 1
        # TODO: probably also need to deal with strings
        else:
            # TODO.  Need a token to have location
            if not isinstance(method, PcValue):
                context.failure = "pc = " + str(context.pc) + \
                    ": Error: must be either a method or a dictionary"
                return
            context.push(PcValue(context.pc + 1))
            context.push("normal")
            context.push(e)
            assert method.pc != context.pc
            context.pc = method.pc

class Labeled_Op:
    def __init__(self, op, file, line, labels):
        self.op = op
        self.file = file
        self.line = line
        self.labels = labels
        self.live_in = set()
        self.live_out = set()

class Code:
    def __init__(self):
        self.labeled_ops = []
        self.endlabels = set()
        self.curFile = None
        self.curLine = 0

    def location(self, file, line):
        self.curFile = file
        self.curLine = line

    def append(self, op, file=None, line=0, labels=set()):
        if file == None:
            file = self.curFile
        if line == 0:
            line = self.curLine
        self.labeled_ops.append(Labeled_Op(op, file, line, labels | self.endlabels))
        self.endlabels = set()

    def nextLabel(self, endlabel):
        self.endlabels.add(endlabel)

    def delete(self, var):
        assert False        # TODO: I think this code is obsolete
        if isinstance(var, tuple):
            self.append(DelVarOp(var))  # remove variable
        else:
            assert isinstance(var, list)
            assert len(var) > 0
            for v in var:
                self.delete(v)

    # This method inserts DelVar operations as soon as a variable is no
    # longer live
    def liveness(self):
        # First figure out what the labels point to and initialize
        # the nodes
        map = {}
        for pc in range(len(self.labeled_ops)):
            lop = self.labeled_ops[pc]
            lop.pred = set()
            lop.live_in = set()
            lop.live_out = set()
            for label in lop.labels:
                assert label not in map, label
                map[label] = pc
        # Compute the predecessors of each node
        for pc in range(len(self.labeled_ops)):
            lop = self.labeled_ops[pc]
            if isinstance(lop.op, JumpOp):
                assert isinstance(lop.op.pc, LabelValue)
                succ = self.labeled_ops[map[lop.op.pc]]
                succ.pred |= {pc}
            elif isinstance(lop.op, JumpCondOp):
                assert pc < len(self.labeled_ops) - 1
                assert isinstance(lop.op.pc, LabelValue)
                succ = self.labeled_ops[map[lop.op.pc]]
                succ.pred |= {pc}
                self.labeled_ops[pc + 1].pred |= {pc}
            elif pc < len(self.labeled_ops) - 1 and not isinstance(lop.op, ReturnOp):
                self.labeled_ops[pc + 1].pred |= {pc}
        # Live variable analysis
        change = True
        while change:
            change = False
            for pc in range(len(self.labeled_ops)):
                lop = self.labeled_ops[pc]
                if pc == len(self.labeled_ops) - 1:
                    live_out = set()
                elif isinstance(lop.op, JumpOp):
                    assert isinstance(lop.op.pc, LabelValue)
                    succ = self.labeled_ops[map[lop.op.pc]]
                    live_out = succ.live_in
                else:
                    live_out = self.labeled_ops[pc + 1].live_in
                    if isinstance(lop.op, JumpCondOp):
                        assert isinstance(lop.op.pc, LabelValue)
                        succ = self.labeled_ops[map[lop.op.pc]]
                        live_out = live_out | succ.live_in
                live_in = lop.op.use() | (live_out - lop.op.define())
                if not change and (live_in != lop.live_in or live_out != lop.live_out):
                    change = True
                lop.live_in = live_in
                lop.live_out = live_out
        # Create new code with DelVars inserted
        newcode = Code()
        for lop in self.labeled_ops:
            # print(lop.op, lop.live_in, lop.live_out)
            file, line = lop.file, lop.line

            # If a variable is live on output of any predecessor but not
            # live on input, delete it first
            lop.pre_del = set()
            for pred in lop.pred:
                plop = self.labeled_ops[pred]
                live_out = plop.live_out | plop.op.define()
                lop.pre_del |= live_out - lop.live_in

            labels = lop.labels
            for d in sorted(lop.pre_del - { 'this' }):
                newcode.append(DelVarOp((d, None, None, None)), file, line, labels)
                labels = set()
            newcode.append(lop.op, file, line, labels)

            # If a variable is defined or live on input but not live on output,
            # immediately delete afterward
            # TODO.  Can optimize StoreVar by replacing it with Pop
            # lop.post_del = (lop.op.define() | lop.live_in) - lop.live_out
            lop.post_del = lop.live_in - lop.live_out
            for d in sorted(lop.post_del - { 'this' }):
                newcode.append(DelVarOp((d, None, None, None)), file, line)

        return newcode

    def link(self):
        map = {}
        for pc in range(len(self.labeled_ops)):
            lop = self.labeled_ops[pc]
            for label in lop.labels:
                assert label not in map, label
                map[label] = PcValue(pc)
        for lop in self.labeled_ops:
            lop.op.substitute(map)

class AST:
    def __init__(self, token, atomically):
        # Check that token is of the form (lexeme, file, line, column)
        assert isinstance(token, tuple), token
        assert len(token) == 4, len(token)
        lexeme, file, line, column = token
        # No check b/c lexeme could be one of many types, e.g. int, str, bool, etc
        # assert isinstance(lexeme, str), lexeme
        assert isinstance(file, str), file
        assert isinstance(line, int), line
        assert isinstance(column, int), line
        self.ast_token = token
        self.atomically = atomically

    # a new local constant or tree of constants
    def define(self, scope, const):
        if isinstance(const, tuple):
            scope.checkUnused(const)
            (lexeme, file, line, column) = const
            scope.names[lexeme] = ("local-const", const)
        else:
            assert isinstance(const, list)
            for c in const:
                self.define(scope, c)

    # a new local variable or tree of variables
    def assign(self, scope, var):
        if isinstance(var, tuple):
            scope.checkUnused(var)
            (lexeme, file, line, column) = var
            scope.names[lexeme] = ("local-var", var)
        else:
            assert isinstance(var, list)
            for v in var:
                self.assign(scope, v)

    def delete(self, scope, code, var):
        assert False        # TODO: I think this is obsolete
        if isinstance(var, tuple):
            code.append(DelVarOp(var))  # remove variable
            (lexeme, file, line, column) = var
            del scope.names[lexeme]
        else:
            assert isinstance(var, list)
            assert len(var) > 0
            for v in var:
                self.delete(scope, code, v)

    def isConstant(self, scope):
        return False

    def eval(self, scope, code):
        state = State(code, scope.labels)
        ctx = ContextValue(("__eval__", None, None, None), 0, novalue, novalue)
        ctx.atomic = 1
        while ctx.pc != len(code.labeled_ops) and ctx.failure == None:
            code.labeled_ops[ctx.pc].op.eval(state, ctx)
        if ctx.failure != None:
            lexeme, file, line, column = self.ast_token
            raise HarmonyCompilerError(
                message='constant evaluation failed: %s %s' % (self, ctx.failure),
                lexeme=lexeme,
                filename=file,
                line=line,
                column=column
            )
        return ctx.pop()

    def compile(self, scope, code):
        if self.isConstant(scope):
            code2 = Code()
            self.gencode(scope, code2)
            v = self.eval(scope, code2)
            code.append(PushOp((v, None, None, None)))
        else:
            self.gencode(scope, code)

    # Return local var name if local access
    def localVar(self, scope):
        assert False, self

    # This is supposed to push the address of an lvalue
    def ph1(self, scope, code):
        lexeme, file, line, column = self.ast_token
        raise HarmonyCompilerError(
            lexeme=lexeme,
            filename=file,
            line=line,
            column=column,
            message='Cannot use in left-hand side expression: %s' % str(self)
        )

    def rec_comprehension(self, scope, code, iter, pc, N, ctype):
        if iter == []:
            (lexeme, file, line, column) = self.token
            if ctype == "list":
                code.append(LoadVarOp(N))
            elif ctype == "dict":
                self.key.compile(scope, code)
            self.value.compile(scope, code)
            if ctype == "set":
                code.append(NaryOp(("SetAdd", file, line, column), 2))
            elif ctype == "dict":
                code.append(NaryOp(("DictAdd", file, line, column), 3))
            elif ctype == "list":
                code.append(NaryOp(("DictAdd", file, line, column), 3))
                code.append(IncVarOp(N))
            elif ctype == "bag":        # TODO.  Probably dead code
                code.append(NaryOp(("BagAdd", file, line, column), 2))
                code.append(IncVarOp(N))
            return

        (type, rest) = iter[0]
        assert type == "for" or type == "where", type

        if type == "for":
            (var, var2, expr) = rest

            self.define(scope, var)
            if var2 != None:
                self.define(scope, var2)
            uid = len(code.labeled_ops)
            (lexeme, file, line, column) = self.token

            # Evaluate the set and store in a temporary variable
            expr.compile(scope, code)
            S = ("$s"+str(uid), file, line, column)
            code.append(StoreVarOp(S))

            # Now generate the code:
            #   while X != {}:
            #       var := oneof X
            #       X := X - var
            #       push value
            global labelcnt
            startlabel = LabelValue(None, "$%d_start"%labelcnt)
            endlabel = LabelValue(None, "$%d_end"%labelcnt)
            labelcnt += 1
            code.nextLabel(startlabel)
            code.append(LoadVarOp(S))
            code.append(NaryOp(("IsEmpty", file, line, column), 1))
            code.append(JumpCondOp(True, endlabel))
            code.append(CutOp(S, var, var2))  
            self.rec_comprehension(scope, code, iter[1:], startlabel, N, ctype)
            code.append(JumpOp(startlabel))
            code.nextLabel(endlabel)

        else:
            assert type == "where"
            negate = isinstance(rest, NaryAST) and rest.op[0] == "not"
            cond = rest.args[0] if negate else rest
            cond.compile(scope, code)
            code.append(JumpCondOp(negate, pc))
            self.rec_comprehension(scope, code, iter[1:], pc, N, ctype)

    def comprehension(self, scope, code, ctype):
        # Keep track of the size
        uid = len(code.labeled_ops)
        (lexeme, file, line, column) = self.token
        N = ("$n"+str(uid), file, line, column)
        if ctype == "set":
            code.append(PushOp((SetValue(set()), file, line, column)))
        elif ctype == "dict":
            code.append(PushOp((novalue, file, line, column)))
        elif ctype in { "bag", "list" }:
            code.append(PushOp((0, file, line, column)))
            code.append(StoreVarOp(N))
            code.append(PushOp((novalue, file, line, column)))
        self.rec_comprehension(scope, code, self.iter, None, N, ctype)
        # if ctype == { "bag", "list" }:
        #     code.append(DelVarOp(N))

    def doImport(self, scope, code, module):
        (lexeme, file, line, column) = module
        # assert lexeme not in scope.names        # TODO
        if lexeme not in imported:
            code.append(PushOp((novalue, file, line, column)))
            code.append(StoreOp(module, module, []))

            # module name replacement with -m flag
            modname = modules[lexeme] if lexeme in modules \
                                else lexeme

            # create a new scope
            scope2 = Scope(None)
            scope2.prefix = [lexeme]
            scope2.labels = scope.labels

            found = False
            install_path = os.path.dirname(os.path.realpath(__file__))
            for dir in [ os.path.dirname(namestack[-1]), install_path + "/modules", "." ]:
                filename = dir + "/" + modname + ".hny"
                if os.path.exists(filename):
                    with open(filename, encoding='utf-8') as f:
                        load(f, filename, scope2, code)
                    found = True
                    break
            if not found:
                raise HarmonyCompilerError(
                    lexeme=modname,
                    filename=str(namestack),
                    line=line, column=column,
                    message="Can't find module %s imported from %s" % (modname, namestack),
                )
            imported[lexeme] = scope2

        scope.names[lexeme] = ("module", imported[lexeme])

    def getLabels(self):
        return set()

    def getImports(self):
        return []

class ConstantAST(AST):
    def __init__(self, const):
        AST.__init__(self, const, False)
        self.const = const

    def __repr__(self):
        return "ConstantAST" + str(self.const)

    def compile(self, scope, code):
        code.append(PushOp(self.const))

    def isConstant(self, scope):
        return True

class NameAST(AST):
    def __init__(self, name):
        AST.__init__(self, name, False)
        self.name = name

    def __repr__(self):
        return "NameAST" + str(self.name)

    def compile(self, scope, code):
        (t, v) = scope.lookup(self.name)
        if t in { "local-var", "local-const" }:
            code.append(LoadVarOp(self.name))
        elif t == "constant":
            (lexeme, file, line, column) = self.name
            code.append(PushOp(v))
        else:
            assert t in { "global", "module" }
            code.append(LoadOp(self.name, self.name, scope.prefix))

    # TODO.  How about local-const?
    def localVar(self, scope):
        (t, v) = scope.lookup(self.name)
        assert t in { "constant", "local-var", "local-const", "global", "module" }
        return self.name[0] if t == "local-var" else None

    def ph1(self, scope, code):
        (t, v) = scope.lookup(self.name)
        if t in { "constant", "local-const" }:
            (lexeme, file, line, column) = v
            raise HarmonyCompilerError(
                filename=file,
                lexeme=lexeme,
                line=line,
                column=column,
                message="constant cannot be an lvalue: %s" % str(self.name),
            )
        elif t == "local-var":
            (lexeme, file, line, column) = v
            if lexeme != "_":
                code.append(PushOp((AddressValue([lexeme]), file, line, column)))
        else:
            (lexeme, file, line, column) = self.name
            code.append(PushOp((AddressValue(scope.prefix + [lexeme]), file, line, column)))

    def ph2(self, scope, code, skip):
        if skip > 0:
            code.append(MoveOp(skip + 2))
            code.append(MoveOp(2))
        (t, v) = scope.lookup(self.name)
        if t == "local-var":
            if self.name[0] == "_":
                code.append(PopOp())
            else:
                code.append(StoreVarOp(None, self.name[0]))
        else:
            assert t == "global", (t, v)
            code.append(StoreOp(None, self.name, None))

    def isConstant(self, scope):
        (lexeme, file, line, column) = self.name
        (t, v) = scope.lookup(self.name)
        if t in { "local-var", "local-const", "global", "module" }:
            return False
        elif t == "constant":
            return not isinstance(v[0], LabelValue)
        else:
            assert False, (t, v, self.name)

class SetAST(AST):
    def __init__(self, token, collection):
        AST.__init__(self, token, False)
        self.collection = collection

    def __repr__(self):
        return str(self.collection)

    def isConstant(self, scope):
        return all(x.isConstant(scope) for x in self.collection)

    def gencode(self, scope, code):
        code.append(PushOp((SetValue(set()), None, None, None)))
        for e in self.collection:
            e.compile(scope, code)
            code.append(NaryOp(("SetAdd", None, None, None), 2))

class RangeAST(AST):
    def __init__(self, lhs, rhs, token):
        AST.__init__(self, token, False)
        self.lhs = lhs
        self.rhs = rhs
        self.token = token

    def __repr__(self):
        return "Range(%s,%s)"%(self.lhs, self.rhs)

    def isConstant(self, scope):
        return self.lhs.isConstant(scope) and self.rhs.isConstant(scope)

    def gencode(self, scope, code):
        self.lhs.compile(scope, code)
        self.rhs.compile(scope, code)
        (lexeme, file, line, column) = self.token
        code.append(NaryOp(("..", file, line, column), 2))

class TupleAST(AST):
    def __init__(self, list, token):
        AST.__init__(self, token, False)
        self.list = list
        self.token = token

    def __repr__(self):
        return "TupleAST" + str(self.list)

    def isConstant(self, scope):
        return all(v.isConstant(scope) for v in self.list)

    def gencode(self, scope, code):
        (lexeme, file, line, column) = self.token
        code.append(PushOp((novalue, file, line, column)))
        for (i, v) in enumerate(self.list):
            code.append(PushOp((i, file, line, column)))
            v.compile(scope, code)
            code.append(NaryOp(("DictAdd", file, line, column), 3))

    def localVar(self, scope):
        lexeme, file, line, column = self.token
        raise HarmonyCompilerError(
            message="Cannot index into tuple in assignment",
            lexeme=lexeme,
            filename=file,
            line=line,
            column=column
        )

    def ph1(self, scope, code):
        for lv in self.list:
            lv.ph1(scope, code)

    def ph2(self, scope, code, skip):
        n = len(self.list)
        code.append(SplitOp(n))
        for lv in reversed(self.list):
            n -= 1
            lv.ph2(scope, code, skip + n)

class DictAST(AST):
    def __init__(self, token, record):
        AST.__init__(self, token, False)
        self.record = record

    def __repr__(self):
        return "DictAST" + str(self.record)

    def isConstant(self, scope):
        return all(k.isConstant(scope) and v.isConstant(scope)
                        for (k, v) in self.record)

    def gencode(self, scope, code):
        code.append(PushOp((novalue, None, None, None)))
        for (k, v) in self.record:
            k.compile(scope, code)
            v.compile(scope, code)
            code.append(NaryOp(("DictAdd", None, None, None), 3))

class SetComprehensionAST(AST):
    def __init__(self, value, iter, token):
        AST.__init__(self, token, False)
        self.value = value
        self.iter = iter
        self.token = token

    def __repr__(self):
        return "SetComprehension(" + str(self.var) + ")"

    def compile(self, scope, code):
        self.comprehension(scope, code, "set")

class DictComprehensionAST(AST):
    def __init__(self, key, value, iter, token):
        AST.__init__(self, token, False)
        self.key = key
        self.value = value
        self.iter = iter
        self.token = token

    def __repr__(self):
        return "DictComprehension(" + str(self.key) + ")"

    def compile(self, scope, code):
        self.comprehension(scope, code, "dict")

class ListComprehensionAST(AST):
    def __init__(self, value, iter, token):
        AST.__init__(self, token, False)
        self.value = value
        self.iter = iter
        self.token = token

    def __repr__(self):
        return "ListComprehension(" + str(self.value) + ")"

    def compile(self, scope, code):
        self.comprehension(scope, code, "list")

# N-ary operator
class NaryAST(AST):
    def __init__(self, op, args):
        AST.__init__(self, op, False)
        self.op = op
        self.args = args
        assert all(isinstance(x, AST) for x in args), args

    def __repr__(self):
        return "NaryOp(" + str(self.op) + ", " + str(self.args) + ")"

    def isConstant(self, scope):
        (op, file, line, column) = self.op
        if op in { "atLabel", "choose", "contexts", "countLabel", "get_context" }:
            return False
        return all(x.isConstant(scope) for x in self.args)

    def gencode(self, scope, code):
        global labelcnt
        (op, file, line, column) = self.op
        n = len(self.args)
        if op == "and" or op == "or":
            self.args[0].compile(scope, code)
            lastlabel = LabelValue(None, "$%d_last"%labelcnt)
            endlabel = LabelValue(None, "$%d_end"%labelcnt)
            labelcnt += 1
            for i in range(1, n):
                code.append(JumpCondOp(op == "or", lastlabel))
                self.args[i].compile(scope, code)
            code.append(JumpOp(endlabel))
            code.nextLabel(lastlabel)
            code.append(PushOp((op == "or", file, line, column)))
            code.nextLabel(endlabel)
        elif op == "=>":
            assert n == 2, n
            self.args[0].compile(scope, code)
            truelabel = LabelValue(None, "$%d_true"%labelcnt)
            endlabel = LabelValue(None, "$%d_end"%labelcnt)
            labelcnt += 1
            code.append(JumpCondOp(False, truelabel))
            self.args[1].compile(scope, code)
            code.append(JumpOp(endlabel))
            code.nextLabel(truelabel)
            code.append(PushOp((True, file, line, column)))
            code.nextLabel(endlabel)
        elif op == "if":
            assert n == 3, n
            negate = isinstance(self.args[1], NaryAST) and self.args[1].op[0] == "not"
            cond = self.args[1].args[0] if negate else self.args[1]
            cond.compile(scope, code)
            elselabel = LabelValue(None, "$%d_else"%labelcnt)
            endlabel = LabelValue(None, "$%d_end"%labelcnt)
            labelcnt += 1
            code.append(JumpCondOp(negate, elselabel))
            self.args[0].compile(scope, code)       # "if" expr
            code.append(JumpOp(endlabel))
            code.nextLabel(elselabel)
            self.args[2].compile(scope, code)       # "else" expr
            code.nextLabel(endlabel)
        elif op == "choose":
            assert n == 1
            self.args[0].compile(scope, code)
            code.append(ChooseOp())
        else:
            for i in range(n):
                self.args[i].compile(scope, code)
            code.append(NaryOp(self.op, n))

class CmpAST(AST):
    def __init__(self, token, ops, args):
        AST.__init__(self, token, False)
        self.ops = ops
        self.args = args
        assert len(ops) == len(args) - 1
        assert all(isinstance(x, AST) for x in args), args

    def __repr__(self):
        return "CmpOp(" + str(self.ops) + ", " + str(self.args) + ")"

    def isConstant(self, scope):
        return all(x.isConstant(scope) for x in self.args)

    def gencode(self, scope, code):
        n = len(self.args)
        self.args[0].compile(scope, code)
        (lexeme, file, line, column) = self.ops[0]
        T = ("__cmp__"+str(len(code.labeled_ops)), file, line, column)
        endlabel = LabelValue(None, "cmp")
        for i in range(1, n-1):
            self.args[i].compile(scope, code)
            code.append(DupOp())
            code.append(StoreVarOp(T))
            code.append(NaryOp(self.ops[i-1], 2))
            code.append(DupOp())
            code.append(JumpCondOp(False, endlabel))
            code.append(PopOp())
            code.append(LoadVarOp(T))
        self.args[n-1].compile(scope, code)
        code.append(NaryOp(self.ops[n-2], 2))
        code.nextLabel(endlabel)
        if n > 2:
            code.append(DelVarOp(T))

class ApplyAST(AST):
    def __init__(self, method, arg, token):
        AST.__init__(self, token, False)
        self.method = method
        self.arg = arg
        self.token = token

    def __repr__(self):
        return "ApplyAST(" + str(self.method) + ", " + str(self.arg) + ")"

    def varCompile(self, scope, code):
        if isinstance(self.method, NameAST):
            (t, v) = scope.lookup(self.method.name)
            if t == "global":
                self.method.ph1(scope, code)
                self.arg.compile(scope, code)
                code.append(AddressOp())
                return True
            else:
                return False

        if isinstance(self.method, PointerAST):
            self.method.expr.compile(scope, code)
            self.arg.compile(scope, code)
            code.append(AddressOp())
            return True

        if isinstance(self.method, ApplyAST):
            if self.method.varCompile(scope, code):
                self.arg.compile(scope, code)
                code.append(AddressOp())
                return True
            else:
                return False

        return False

    def compile(self, scope, code):
        if isinstance(self.method, NameAST):
            (t, v) = scope.lookup(self.method.name)
            # See if it's of the form "module.constant":
            if t == "module" and isinstance(self.arg, ConstantAST) and isinstance(self.arg.const[0], str):
                (t2, v2) = v.lookup(self.arg.const)
                if t2 == "constant":
                    code.append(PushOp(v2))
                    return
            # Decrease chances of data race
            if t == "global":
                self.method.ph1(scope, code)
                self.arg.compile(scope, code)
                code.append(AddressOp())
                code.append(LoadOp(None, self.token, None))
                return

        # Decrease chances of data race
        if self.varCompile(scope, code):
            code.append(LoadOp(None, self.token, None))
            return

        self.method.compile(scope, code)
        self.arg.compile(scope, code)
        code.append(ApplyOp(self.token))

    def localVar(self, scope):
        return self.method.localVar(scope)

    def ph1(self, scope, code):
        # See if it's of the form "module.constant":
        if isinstance(self.method, NameAST):
            (t, v) = scope.lookup(self.method.name)
            if t == "module" and isinstance(self.arg, ConstantAST) and isinstance(self.arg.const[0], str):
                (t2, v2) = v.lookup(self.arg.const)
                if t2 == "constant":
                    lexeme, file, line, column = self.ast_token
                    raise HarmonyCompilerError(
                        message="Cannot assign to constant %s %s" % (self.method.name, self.arg.const),
                        lexeme=lexeme,
                        filename=file,
                        line=line,
                        column=column
                    )
        self.method.ph1(scope, code)
        self.arg.compile(scope, code)
        code.append(AddressOp())

    def ph2(self, scope, code, skip):
        if skip > 0:
            code.append(MoveOp(skip + 2))
            code.append(MoveOp(2))
        lvar = self.method.localVar(scope)
        st = StoreOp(None, self.token, None) if lvar == None else StoreVarOp(None, lvar)
        code.append(st)

class Rule:
    def expect(self, rule, b, got, want):
        if not b:
            lexeme, file, line, column = got
            raise HarmonyCompilerError(
                lexeme=lexeme,
                filename=file,
                line=line,
                column=column,
                message="Parse error in %s. Got %s, but %s" % (rule, got, want)
            )

    def forParse(self, t, closers):
        (bv, t) = BoundVarRule().parse(t)
        (lexeme, file, line, column) = token = t[0]
        if lexeme == ":":
            (bv2, t) = BoundVarRule().parse(t[1:])
            (lexeme, file, line, column) = token = t[0]
        else:
            bv2 = None
        self.expect("for expression", lexeme == "in", t[0], "expected 'in'")
        (expr, t) = NaryRule(closers | { "where", "for" }).parse(t[1:])
        if bv2 == None:
            return ((bv, None, expr), t)
        else:
            return ((bv2, bv, expr), t)

    def whereParse(self, t, closers):
        return NaryRule(closers | { "for", "where" }).parse(t)

    def iterParse(self, t, closers):
        (ve, t) = self.forParse(t, closers)
        lst = [("for", ve)]
        (lexeme, file, line, column) = t[0]
        while lexeme not in closers:
            self.expect("for expression", lexeme == "for" or lexeme == "where",
                            lexeme, "expected 'for' or 'where'")
            if lexeme == "for":
                (ve, t) = self.forParse(t[1:], closers)
                lst.append(("for", ve))
            else:
                assert lexeme == "where"
                (st, t) = self.whereParse(t[1:], closers)
                lst.append(("where", st))
            (lexeme, file, line, column) = t[0]
        return (lst, t)

class NaryRule(Rule):
    def __init__(self, closers):
        self.closers = closers

    def parse(self, t):
        (ast, t) = ExpressionRule().parse(t)
        if ast == False or t == []:
            return (ast, t)
        (lexeme, file, line, column) = t[0]
        if lexeme in self.closers:
            return (ast, t)
        args = [ast]
        op = t[0]
        invert = None
        if isunaryop(op[0]) and op[0] != '-':  # mostly for use in "a not in s", but more general
            invert = op
            t = t[1:]
            op = t[0]
        self.expect("n-ary operation", isbinaryop(op[0]) or op[0] == "if", op,
                    "expected binary operation or 'if'")
        if iscmpop(op[0]):
            assert invert == None           # TODO
            ops = []
            while iscmpop(lexeme):
                ops.append(t[0])
                (ast3, t) = ExpressionRule().parse(t[1:])
                if ast3 == False:
                    lexeme, file, line, column = t[0] if t else (lexeme, file, line, column)
                    raise HarmonyCompilerError(
                        filename=file,
                        line=line,
                        column=column,
                        lexeme=lexeme,
                        message="expected an expression after n-ary comparison operation in %s" % str(op)
                    )
                args.append(ast3)
                if t == []:
                    break
                (lexeme, file, line, column) = t[0]
            if t != []:
                self.expect("n-ary operation", lexeme in self.closers,
                        t[0], "expected one of %s"%self.closers)
            return (CmpAST(op, ops, args), t)
        if op[0] == "if":
            (ast2, t) = NaryRule({"else"}).parse(t[1:])
        else:
            (ast2, t) = ExpressionRule().parse(t[1:])
        if ast2 == False:
            lexeme, file, line, column = t[0] if t else (lexeme, file, line, column)
            raise HarmonyCompilerError(
                filename=file,
                lexeme=lexeme,
                line=line,
                column=column,
                message="expected an expression after operation %s" % str(op)
            )
        args.append(ast2)
        if t != []:
            (lexeme, file, line, column) = t[0]
            if op[0] == "if":
                self.expect("n-ary operation", lexeme == "else", t[0], "expected 'else'")
                (ast3, t) = ExpressionRule().parse(t[1:])
                if ast3 == False:
                    lexeme, file, line, column = t[0] if t else (lexeme, file, line, column)
                    raise HarmonyCompilerError(
                        filename=file,
                        lexeme=lexeme,
                        line=line,
                        column=column,
                        message="expected an expression after else in %s" % str(op)
                    )
                args.append(ast3)
                if t != []:
                    (lexeme, file, line, column) = t[0]
            elif (op[0] == lexeme) and (lexeme in { "+", "*", "|", "&", "^", "and", "or" }):
                while lexeme == op[0]:
                    (ast3, t) = ExpressionRule().parse(t[1:])
                    if ast3 == False:
                        lexeme, file, line, column = t[0] if t else (lexeme, file, line, column)
                        raise HarmonyCompilerError(
                            filename=file,
                            lexeme=lexeme,
                            line=line,
                            column=column,
                            message="expected an expression after n-ary operation in %s" % str(op)
                        )
                    args.append(ast3)
                    if t == []:
                        break
                    (lexeme, file, line, column) = t[0]
            if t != []:
                self.expect("n-ary operation", lexeme in self.closers, t[0],
                                "expected one of %s"%self.closers)
        ast = NaryAST(op, args)
        if invert != None:
            return (NaryAST(invert, [ast]), t)
        else:
            return (ast, t)

class SetComprehensionRule(Rule):
    def __init__(self, value, terminator):
        self.value = value
        self.terminator = terminator

    def parse(self, t):
        token = t[0]
        (lst, t) = self.iterParse(t[1:], {self.terminator})
        return (SetComprehensionAST(self.value, lst, token), t[1:])

class DictComprehensionRule(Rule):
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def parse(self, t):
        token = t[0]
        (lst, t) = self.iterParse(t[1:], {"}"})
        return (DictComprehensionAST(self.key, self.value, lst, token), t[1:])

class ListComprehensionRule(Rule):
    def __init__(self, value, closers):
        self.value = value
        self.closers = closers

    def parse(self, t):
        token = t[0]
        (lst, t) = self.iterParse(t[1:], self.closers) 
        return (ListComprehensionAST(self.value, lst, token), t)

class SetRule(Rule):
    def parse(self, t):
        first_token = t[0]
        (lexeme, file, line, column) = t[0]
        self.expect("set expression", lexeme == "{", t[0], "expected '{'")
        (lexeme, file, line, column) = t[1]
        if lexeme == "}":
            return (SetAST(first_token, []), t[2:])
        s = []
        while True:
            (next, t) = NaryRule({":", "for", "..", ",", "}"}).parse(t[1:])
            if next == False:
                return (False, t)
            s.append(next)
            (lexeme, file, line, column) = t[0]
            if lexeme == ":":
                self.expect("set/dict", len(s) == 1, t[0],
                            "cannot mix set values and value maps")
                return DictSuffixRule(s[0]).parse(t[1:])
            if lexeme == "for":
                self.expect("set comprehension", len(s) == 1, t[0],
                    "can have only one expression")
                return SetComprehensionRule(s[0], '}').parse(t)
            if lexeme == "..":
                self.expect("range", len(s) == 1, t[0],
                    "can have only two expressions")
                token = t[0]
                (ast, t) = NaryRule({"}"}).parse(t[1:])
                return (RangeAST(next, ast, token), t[1:])
            if lexeme == "}":
                return (SetAST(first_token, s), t[1:])
            self.expect("set expression", lexeme == ",", t[0],
                    "expected a comma")

class DictSuffixRule(Rule):
    def __init__(self, first):
        self.first = first

    def parse(self, t):
        key = self.first
        d = []
        while True:
            (value, t) = NaryRule({",", "}", "for"}).parse(t)
            (lexeme, file, line, column) = t[0]
            self.expect("dict expression", lexeme in { ",", "}", "for" }, t[0],
                                    "expected a comma or '}'")
            if lexeme == "for":
                self.expect("dict comprehension", d == [], t[0],
                    "expected single expression")
                return DictComprehensionRule(key, value).parse(t)

            d.append((key, value))
            if lexeme == "}":
                return (DictAST(t[0], d), t[1:])

            (key, t) = NaryRule({":"}).parse(t[1:])
            if key == False:
                return (key, t)
            (lexeme, file, line, column) = t[0]
            self.expect("dict expression", lexeme == ":", t[0],
                                        "expected a colon")
            t = t[1:]

class TupleRule(Rule):
    def __init__(self, closers):
        self.closers = closers

    def parse(self, t):
        (lexeme, file, line, column) = t[0]
        if lexeme in self.closers:
            return (ConstantAST(
                (novalue, file, line, column)), t)
        (ast, t) = NaryRule(self.closers.union({",", "for"})).parse(t)
        if not ast or t == []:
            return (ast, t)
        (lexeme, file, line, column) = token = t[0]
        if lexeme in self.closers:
            return (ast, t)
        if lexeme == "for":
            return ListComprehensionRule(ast, self.closers).parse(t)
        d = [ ast ]
        while lexeme == ",":
            (lexeme, file, line, column) = t[1]
            if lexeme in self.closers:
                return (TupleAST(d, token), t[1:])
            (next, t) = NaryRule(self.closers.union({ "," })).parse(t[1:])
            d.append(next)
            if t == []:
                break
            (lexeme, file, line, column) = token = t[0]
        if t != []:
            self.expect("tuple expression", lexeme in self.closers, t[0],
                "expected %s"%self.closers)
        return (TupleAST(d, token), t)

class BasicExpressionRule(Rule):
    def parse(self, t):
        (lexeme, file, line, column) = token = t[0]
        if isnumber(lexeme):
            return (ConstantAST((int(lexeme), file, line, column)), t[1:])
        if lexeme == "False":
            return (ConstantAST((False, file, line, column)), t[1:])
        if lexeme == "True":
            return (ConstantAST((True, file, line, column)), t[1:])
        if lexeme == "None":
            return (ConstantAST((AddressValue([]), file, line, column)), t[1:])
        if lexeme == "inf":
            return (ConstantAST((math.inf, file, line, column)), t[1:])
        if lexeme[0] == '"':
            return (ConstantAST((lexeme[1:], file, line, column)), t[1:])
            # return (TupleAST([ ConstantAST((c, file, line, column))
            #                   for c in lexeme[1:] ], token), t[1:])
        if lexeme == ".": 
            (lexeme, file, line, column) = t[1]
            if lexeme.startswith("0x"):
                return (ConstantAST((chr(int(lexeme, 16)), file, line, column)), t[2:])
            else:
                self.expect("dot expression", isname(lexeme), t[1],
                    "expected a name after .")
                return (ConstantAST((lexeme, file, line, column)), t[2:])
        if isname(lexeme):
            return (NameAST(t[0]), t[1:])
        if lexeme == "{":
            return SetRule().parse(t)
        if lexeme == "(" or lexeme == "[":
            closer = ")" if lexeme == "(" else "]"
            (ast, t) = TupleRule({closer}).parse(t[1:])
            return (ast, t[1:])
        if lexeme == "?":
            (ast, t) = ExpressionRule().parse(t[1:])
            return (AddressAST(token, ast), t)
        return (False, t)

class PointerAST(AST):
    def __init__(self, expr, token):
        AST.__init__(self, token, False)
        self.expr = expr
        self.token = token

    def __repr__(self):
        return "PointerAST(" + str(self.expr) + ")"

    def compile(self, scope, code):
        self.expr.compile(scope, code)
        code.append(LoadOp(None, self.token, None))

    def localVar(self, scope):
        return None

    def ph1(self, scope, code):
        self.expr.compile(scope, code)

    def ph2(self, scope, code, skip):
        if skip > 0:
            code.append(MoveOp(skip + 2))
            code.append(MoveOp(2))
        code.append(StoreOp(None, self.token, None))

class ExpressionRule(Rule):
    def parse(self, t):
        func = t[0]
        (lexeme, file, line, column) = func
        if lexeme == "lambda":
            (bv, t) = BoundVarRule().parse(t[1:])
            (lexeme, file, line, column) = t[0]
            self.expect("lambda expression", lexeme == ":", t[0], "expected ':'")
            (ast, t) = NaryRule(["end"]).parse(t[1:])
            return (LambdaAST(bv, ast, func), t[1:])
        if lexeme == "setintlevel":
            (ast, t) = ExpressionRule().parse(t[1:])
            return (SetIntLevelAST(func, ast), t)
        if lexeme == "save":
            (ast, t) = ExpressionRule().parse(t[1:])
            return (SaveAST(func, ast), t)
        if lexeme == "stop":
            (ast, t) = ExpressionRule().parse(t[1:])
            return (StopAST(func, ast), t)
        if isunaryop(lexeme):
            (ast, t) = ExpressionRule().parse(t[1:])
            if lexeme == "!":
                return (PointerAST(ast, func), t)
            else:
                return (NaryAST(func, [ast]), t)

        # Example:
        # a b c -> d e -> f
        # (a b c -> d e) -> f
        # ((a b c -> d) e) -> f
        # (((a b c) -> d) e) -> f
        # ((((a b) c) -> d) e) -> f
        (ast, t) = BasicExpressionRule().parse(t)
        while t != []:
            (lexeme, file, line, column) = t[0]
            if lexeme == "->":
                (lexeme, file, line, column) = t[1]
                self.expect("-> expression", isname(lexeme), t[1],
                        "expected a name after ->")
                ast = ApplyAST(PointerAST(ast, t[1]), ConstantAST(t[1]), t[1])
                t = t[2:]
                if t == []:
                    break
            else:
                (arg, t) = BasicExpressionRule().parse(t)
                if arg == False:
                    break
                ast = ApplyAST(ast, arg, func)
        return (ast, t)

class AssignmentAST(AST):
    def __init__(self, lhslist, rv, op, atomically):
        AST.__init__(self, op, atomically)
        self.lhslist = lhslist      # a, b = c, d = e = ...
        self.rv = rv                # rhs expression
        self.op = op                # ... op= ...

    def __repr__(self):
        return "Assignment(" + str(self.lhslist) + ", " + str(self.rv) + \
                            ", " + str(self.op) + ")"

    # handle an "x op= y" assignment
    def opassign(self, lv, scope, code):
        if self.atomically:
            code.append(AtomicIncOp(True))
        lvar = lv.localVar(scope)
        if isinstance(lv, NameAST):
            # handled separately for assembly code readability
            (t, v) = scope.lookup(lv.name)
            lexeme, file, line, column = self.ast_token
            if t == "module":
                raise HarmonyCompilerError(
                    filename=file,
                    lexeme=lexeme,
                    line=line,
                    column=column,
                    message='Cannot operate on module %s' % str(lv.name),
                )
            if t in { "constant", "local-const" }:
                raise HarmonyCompilerError(
                    filename=file,
                    lexeme=lexeme,
                    line=line,
                    column=column,
                    message='Cannot operate on constant %s' % str(lv.name),
                )
            assert t in { "local-var", "global" }
            ld = LoadOp(lv.name, lv.name, scope.prefix) if t == "global" else LoadVarOp(lv.name)
        else:
            lv.ph1(scope, code)
            code.append(DupOp())                  # duplicate the address
            ld = LoadOp(None, self.op, None) if lvar == None else LoadVarOp(None, lvar)
        code.append(ld)                       # load the value
        self.rv.compile(scope, code)          # compile the rhs
        (lexeme, file, line, column) = self.op
        code.append(NaryOp((lexeme[:-1], file, line, column), 2))
        if isinstance(lv, NameAST):
            st = StoreOp(lv.name, lv.name, scope.prefix) if lvar == None else StoreVarOp(lv.name, lvar)
        else:
            st = StoreOp(None, self.op, None) if lvar == None else StoreVarOp(None, lvar)
        code.append(st)
        if self.atomically:
            code.append(AtomicDecOp())

    def compile(self, scope, code):
        (lexeme, file, line, column) = self.op
        if lexeme != '=':
            assert len(self.lhslist) == 1, self.lhslist
            lv = self.lhslist[0]
            self.opassign(lv, scope, code)
            return

        if self.atomically:
            code.append(AtomicIncOp(True))

        # Compute the addresses of lhs expressions
        for lvs in self.lhslist:
            # handled separately for better assembly code readability
            if not isinstance(lvs, NameAST):
                lvs.ph1(scope, code)

        # Compute the right-hand side
        self.rv.compile(scope, code)

        # Make enough copies for each left-hand side
        for i in range(len(self.lhslist) - 1):
            code.append(DupOp())

        # Now assign to the left-hand side in reverse order
        skip = len(self.lhslist)
        for lvs in reversed(self.lhslist):
            skip -= 1
            if isinstance(lvs, NameAST):
                (t, v) = scope.lookup(lvs.name)
                if t == "module":
                    raise HarmonyCompilerError(
                        lexeme=lexeme,
                        filename=file,
                        line=line,
                        column=column,
                        message='Cannot assign to module %s' % str(lvs.name),
                    )
                if t in { "constant", "local-const" }:
                    raise HarmonyCompilerError(
                        lexeme=lexeme,
                        filename=file,
                        line=line,
                        column=column,
                        message='Cannot assign to constant %s' % str(lvs.name),
                    )
                assert t in { "local-var", "global" }, (t, lvs.name)
                if v[0] == "_":
                    code.append(PopOp())
                else:
                    st = StoreOp(lvs.name, lvs.name, scope.prefix) if t == "global" else StoreVarOp(lvs.name)
                    code.append(st)
            else:
                lvs.ph2(scope, code, skip)

        if self.atomically:
            code.append(AtomicDecOp())

class DelAST(AST):
    def __init__(self, token, atomically, lv):
        AST.__init__(self, token, atomically)
        self.lv = lv

    def __repr__(self):
        return "Del(" + str(self.lv) + ")"

    def compile(self, scope, code):
        if self.atomically:
            code.append(AtomicIncOp(True))
        lvar = self.lv.localVar(scope)
        if isinstance(self.lv, NameAST):
            op = DelOp(self.lv.name, scope.prefix) if lvar == None else DelVarOp(self.lv.name)
        else:
            self.lv.ph1(scope, code)
            op = DelOp(None, None) if lvar == None else DelVarOp(None, lvar)
        code.append(op)
        if self.atomically:
            code.append(AtomicDecOp())

class SetIntLevelAST(AST):
    def __init__(self, token, arg):
        AST.__init__(self, token, False)
        self.arg = arg

    def __repr__(self):
        return "SetIntLevel " + str(self.arg)

    def compile(self, scope, code):
        self.arg.compile(scope, code)
        code.append(SetIntLevelOp())

class SaveAST(AST):
    def __init__(self, token, expr):
        AST.__init__(self, token, False)
        self.expr = expr

    def __repr__(self):
        return "Save " + str(self.expr)

    def compile(self, scope, code):
        self.expr.compile(scope, code)
        code.append(SaveOp())
        code.append(ContinueOp())

class StopAST(AST):
    def __init__(self, token, expr):
        AST.__init__(self, token, False)
        self.expr = expr

    def __repr__(self):
        return "Stop " + str(self.expr)

    def compile(self, scope, code):
        # self.expr.ph1(scope, code)
        self.expr.compile(scope, code)
        code.append(StopOp(None))
        code.append(ContinueOp())

class AddressAST(AST):
    def __init__(self, token, lv):
        AST.__init__(self, token, False)
        self.lv = lv

    def __repr__(self):
        return "Address(" + str(self.lv) + ")"

    def isConstant(self, scope):
        return self.lv.isConstant(scope)

    def check(self, lv, scope):
        if isinstance(lv, NameAST):
            (t, v) = scope.lookup(lv.name)
            lexeme, file, line, column = lv.name
            if t in { "local-var", "local-const" }:
                raise HarmonyCompilerError(
                    filename=file,
                    lexeme=lexeme,
                    line=line,
                    column=column,
                    message="Can't take address of local variable %s" % str(lv),
                )
            if t == "constant":
                raise HarmonyCompilerError(
                    filename=file,
                    lexeme=lexeme,
                    line=line,
                    column=column,
                    message="Can't take address of constant %s" % str(lv),
                )
            if t == "module":
                raise HarmonyCompilerError(
                    filename=file,
                    lexeme=lexeme,
                    line=line,
                    column=column,
                    message="Can't take address of imported %s" % str(lv),
                )
        elif isinstance(lv, ApplyAST):
            self.check(lv.method, scope)
        elif isinstance(lv, PointerAST):
            pass
        else:
            lexeme, file, line, column = lv.ast_token if isinstance(lv, AST) else (None, None, None, None)
            raise HarmonyCompilerError(
                filename=file,
                lexeme=lexeme,
                line=line,
                column=column,
                message="Can't take address of %s" % str(lv),
            )

    def gencode(self, scope, code):
        self.check(self.lv, scope)
        self.lv.ph1(scope, code)

class PassAST(AST):
    def __init__(self, token, atomically):
        AST.__init__(self, token, atomically)

    def __repr__(self):
        return "Pass"

    def compile(self, scope, code):
        pass

class BlockAST(AST):
    def __init__(self, token, atomically, b):
        AST.__init__(self, token, atomically)
        assert len(b) > 0
        self.b = b

    def __repr__(self):
        return "Block(" + str(self.b) + ")"

    def compile(self, scope, code):
        ns = Scope(scope)
        for s in self.b:
            for ((lexeme, file, line, column), lb) in s.getLabels():
                ns.names[lexeme] = ("constant", (lb, file, line, column))
        if self.atomically:
            code.append(AtomicIncOp(True))
        for s in self.b:
            s.compile(ns, code)
        if self.atomically:
            code.append(AtomicDecOp())

    def getLabels(self):
        labels = [ x.getLabels() for x in self.b ]
        return functools.reduce(lambda x,y: x|y, labels)

    def getImports(self):
        imports = [ x.getImports() for x in self.b ]
        return functools.reduce(lambda x,y: x+y, imports)

class IfAST(AST):
    def __init__(self, token, atomically, alts, stat):
        AST.__init__(self, token, atomically)
        self.alts = alts        # alternatives
        self.stat = stat        # else statement

    def __repr__(self):
        return "If(" + str(self.alts) + ", " + str(self.stat) + ")"

    def compile(self, scope, code):
        global labelcnt
        label = labelcnt
        labelcnt += 1
        sublabel = 0
        endlabel = LabelValue(None, "$%d_end"%label)
        if self.atomically:
            code.append(AtomicIncOp(True))
        last = len(self.alts) - 1
        for i, alt in enumerate(self.alts):
            (rest, stat, thefile, theline) = alt
            code.location(thefile, theline)
            negate = isinstance(rest, NaryAST) and rest.op[0] == "not"
            cond = rest.args[0] if negate else rest
            cond.compile(scope, code)
            iflabel = LabelValue(None, "$%d_%d"%(label, sublabel))
            code.append(JumpCondOp(negate, iflabel))
            sublabel += 1
            stat.compile(scope, code)
            if self.stat != None or i != last:
                code.append(JumpOp(endlabel))
            code.nextLabel(iflabel)
        if self.stat != None:
            self.stat.compile(scope, code)
        code.nextLabel(endlabel)
        if self.atomically:
            code.append(AtomicDecOp())

    def getLabels(self):
        labels = [ x.getLabels() for (c, x, _, _) in self.alts ]
        if self.stat != None:
            labels += [ self.stat.getLabels() ]
        return functools.reduce(lambda x,y: x|y, labels)

    def getImports(self):
        imports = [ x.getImports() for (c, x, _, _) in self.alts ]
        if self.stat != None:
            imports += [ self.stat.getImports() ]
        return functools.reduce(lambda x,y: x+y, imports)

class WhileAST(AST):
    def __init__(self, token, atomically, cond, stat):
        AST.__init__(self, token, atomically)
        self.cond = cond
        self.stat = stat

    def __repr__(self):
        return "While(" + str(self.cond) + ", " + str(self.stat) + ")"

    def compile(self, scope, code):
        if self.atomically:
            code.append(AtomicIncOp(True))
        negate = isinstance(self.cond, NaryAST) and self.cond.op[0] == "not"
        cond = self.cond.args[0] if negate else self.cond
        global labelcnt
        startlabel = LabelValue(None, "$%d_start"%labelcnt)
        endlabel = LabelValue(None, "$%d_end"%labelcnt)
        labelcnt += 1
        code.nextLabel(startlabel)
        cond.compile(scope, code)
        code.append(JumpCondOp(negate, endlabel))
        self.stat.compile(scope, code)
        code.append(JumpOp(startlabel))
        code.nextLabel(endlabel)
        if self.atomically:
            code.append(AtomicDecOp())

    def getLabels(self):
        return self.stat.getLabels()

    def getImports(self):
        return self.stat.getImports()

class InvariantAST(AST):
    def __init__(self, cond, token, atomically):
        AST.__init__(self, token, atomically)
        self.cond = cond
        self.token = token

    def __repr__(self):
        return "Invariant(" + str(self.cond) + ")"

    def compile(self, scope, code):
        global labelcnt
        label = LabelValue(None, "$%d"%labelcnt)
        labelcnt += 1
        code.append(InvariantOp(label, self.token))
        self.cond.compile(scope, code)

        # TODO. The following is a workaround for a bug.
        # When you do "invariant 0 <= count <= 1", it inserts
        # DelVar operations before the ReturnOp, and the InvariantOp
        # operation then jumps to the wrong instruction
        code.append(ContinueOp())

        code.nextLabel(label)
        code.append(ReturnOp())

class LetAST(AST):
    def __init__(self, token, atomically, vars, stat):
        AST.__init__(self, token, atomically)
        self.vars = vars
        self.stat = stat

    def __repr__(self):
        return "Let(" + str(self.vars) + ", " + str(self.stat) + ")"

    def compile(self, scope, code):
        if self.atomically:
            code.append(AtomicIncOp(True))
        ns = Scope(scope)
        for (var, expr) in self.vars:
            expr.compile(ns, code)
            code.append(StoreVarOp(var))
            self.define(ns, var)

        # Run the body
        self.stat.compile(ns, code)

        if self.atomically:
            code.append(AtomicDecOp())

class VarAST(AST):
    def __init__(self, token, atomically, vars):
        AST.__init__(self, token, atomically)
        self.vars = vars

    def __repr__(self):
        return "Var(" + str(self.vars) + ")"

    def compile(self, scope, code):
        if self.atomically:
            code.append(AtomicIncOp(True))
        for (var, expr) in self.vars:
            expr.compile(scope, code)
            code.append(StoreVarOp(var))
            self.assign(scope, var)
        if self.atomically:
            code.append(AtomicDecOp())

class ForAST(AST):
    def __init__(self, iter, stat, token, atomically):
        AST.__init__(self, token, atomically)
        self.value = stat
        self.iter = iter
        self.token = token

    def __repr__(self):
        return "For(" + str(self.iter) + ", " + str(self.stat) + ")"

    def compile(self, scope, code):
        if self.atomically:
            code.append(AtomicIncOp(True))
        ns = Scope(scope)
        self.comprehension(ns, code, "for")
        if self.atomically:
            code.append(AtomicDecOp())

    def getLabels(self):
        return self.value.getLabels()

    def getImports(self):
        return self.value.getImports()

class LetWhenAST(AST):
    # vars_and_conds, a list of one of
    #   - ('var', bv, ast)              // let bv = ast
    #   - ('cond', cond)                // when cond:
    #   - ('exists', bv, expr)    // when exists bv in expr
    def __init__(self, token, atomically, vars_and_conds, stat):
        AST.__init__(self, token, atomically)
        self.token = token
        self.vars_and_conds = vars_and_conds
        self.stat = stat

    def __repr__(self):
        return "LetWhen(" + str(self.vars_and_conds) + ", " + str(self.stat) + ")"

    def compile(self, scope, code):
        """
        start:
            atomic inc
            [[let1]]
            [[cond1]]
            jump condfailed if false
            ...
            [[letn]]
            [[condn]]
            jump condfailed if false
            jump body
        condfailed:
            atomic dec
            jump start
        select:
            choose
            storevar bv
        body:
            [[stmt]]
            atomic dec
        """

        # declare labels
        global labelcnt
        label_start = LabelValue(None, "LetWhenAST_start$%d"%labelcnt)
        labelcnt += 1
        label_condfailed = LabelValue(None, "LetWhenAST_condfailed$%d"%labelcnt)
        labelcnt += 1
        label_body = LabelValue(None, "LetWhenAST_body$%d"%labelcnt)
        labelcnt += 1

        # start:
        code.nextLabel(label_start)
        if self.atomically:
            code.append(AtomicIncOp(True))
            code.append(ReadonlyIncOp())
        ns = Scope(scope)
        for var_or_cond in self.vars_and_conds:
            if var_or_cond[0] == 'var':
                var, expr = var_or_cond[1:]
                expr.compile(ns, code)
                code.append(StoreVarOp(var))
                self.define(ns, var)
            elif var_or_cond[0] == 'cond':
                cond = var_or_cond[1]
                cond.compile(ns, code)
                code.append(JumpCondOp(False, label_condfailed))
            else:
                assert var_or_cond[0] == 'exists'
                (_, bv, expr) = var_or_cond
                (_, file, line, column) = self.token
                self.define(ns, bv)
                expr.compile(ns, code)
                code.append(DupOp())
                code.append(PushOp((SetValue(set()), file, line, column)))
                code.append(NaryOp(("==", file, line, column), 2))
                label_select = LabelValue(None, "LetWhenAST_select$%d"%labelcnt)
                labelcnt += 1
                code.append(JumpCondOp(False, label_select))

                # set is empty.  Try again
                code.append(PopOp())
                if self.atomically:
                    code.append(ReadonlyDecOp())
                    code.append(AtomicDecOp())
                code.append(JumpOp(label_start))

                # select:
                code.nextLabel(label_select)
                code.append(ChooseOp())
                code.append(StoreVarOp(bv))
        code.append(JumpOp(label_body))

        # condfailed:
        code.nextLabel(label_condfailed)
        if self.atomically:
            code.append(ReadonlyDecOp())
            code.append(AtomicDecOp())
        code.append(JumpOp(label_start))

        # body:
        code.nextLabel(label_body)
        if self.atomically:
            code.append(ReadonlyDecOp())
        self.stat.compile(ns, code)
        if self.atomically:
            code.append(AtomicDecOp())

    def getLabels(self):
        return self.stat.getLabels()

    def getImports(self):
        return self.stat.getImports()

class AtomicAST(AST):
    def __init__(self, token, atomically, stat):
        AST.__init__(self, token, atomically)
        self.stat = stat

    def __repr__(self):
        return "Atomic(" + str(self.stat) + ")"

    def compile(self, scope, code):
        code.append(AtomicIncOp(True))
        self.stat.compile(scope, code)
        code.append(AtomicDecOp())

    # TODO.  Is it ok to define labels within an atomic block?
    def getLabels(self):
        return self.stat.getLabels()

    def getImports(self):
        return self.stat.getImports()

class AssertAST(AST):
    def __init__(self, token, atomically, cond, expr):
        AST.__init__(self, token, atomically)
        self.token = token
        self.cond = cond
        self.expr = expr

    def __repr__(self):
        return "Assert(" + str(self.token) + ", " + str(self.cond) + ", " + str(self.expr) + ")"

    def compile(self, scope, code):
        code.append(ReadonlyIncOp())
        code.append(AtomicIncOp(True))
        self.cond.compile(scope, code)
        if self.expr != None:
            self.expr.compile(scope, code)
        code.append(AssertOp(self.token, self.expr != None))
        code.append(AtomicDecOp())
        code.append(ReadonlyDecOp())

class PrintAST(AST):
    def __init__(self, token, atomically, expr):
        AST.__init__(self, token, atomically)
        self.token = token
        self.expr = expr

    def __repr__(self):
        return "Print(" + str(self.token) + ", " + str(self.expr) + ")"

    def compile(self, scope, code):
        self.expr.compile(scope, code)
        code.append(PrintOp(self.token))

class PossiblyAST(AST):
    def __init__(self, token, atomically, condlist):
        AST.__init__(self, token, atomically)
        self.token = token
        self.condlist = condlist

    def __repr__(self):
        return "Possibly()"

    def compile(self, scope, code):
        code.append(ReadonlyIncOp())
        code.append(AtomicIncOp(True))
        for i, cond in enumerate(self.condlist):
            cond.compile(scope, code)
            code.append(PossiblyOp(self.token, i))
        code.append(AtomicDecOp())
        code.append(ReadonlyDecOp())

class MethodAST(AST):
    def __init__(self, token, atomically, name, args, stat):
        AST.__init__(self, token, atomically)
        self.name = name
        self.args = args
        self.stat = stat
        (lexeme, file, line, column) = name
        self.label = LabelValue(None, lexeme)

    def __repr__(self):
        return "Method(" + str(self.name) + ", " + str(self.args) + ", " + str(self.stat) + ")"

    def compile(self, scope, code):
        global labelcnt
        endlabel = LabelValue(None, "$%d"%labelcnt)
        labelcnt += 1
        (lexeme, file, line, column) = self.name
        code.append(JumpOp(endlabel))
        code.nextLabel(self.label)
        code.append(FrameOp(self.name, self.args))
        # scope.names[lexeme] = ("constant", (self.label, file, line, column))

        ns = Scope(scope)
        for ((lexeme, file, line, column), lb) in self.stat.getLabels():
            ns.names[lexeme] = ("constant", (lb, file, line, column))
        self.define(ns, self.args)
        ns.names["result"] = ("local-var", ("result", file, line, column))
        if self.atomically:
            code.append(AtomicIncOp(True))
        self.stat.compile(ns, code)
        if self.atomically:
            code.append(AtomicDecOp())
        code.append(ReturnOp())
        code.nextLabel(endlabel)

        # promote global variables
        for name, (t, v) in ns.names.items():
            if t == "global" and name not in scope.names:
                scope.names[name] = (t, v)

    def getLabels(self):
        return { (self.name, self.label) } | self.stat.getLabels()

    def getImports(self):
        return self.stat.getImports()

class LambdaAST(AST):
    def __init__(self, args, stat, token, atomically):
        AST.__init__(self, token, atomically)
        self.args = args
        self.stat = stat
        self.token = token

    def __repr__(self):
        return "Lambda " + str(self.args) + ", " + str(self.stat) + ")"

    def isConstant(self, scope):
        return True

    def compile_body(self, scope, code):
        startlabel = LabelValue(None, "lambda")
        endlabel = LabelValue(None, "lambda")
        code.append(JumpOp(endlabel))
        code.nextLabel(startlabel)
        code.append(FrameOp(self.token, self.args))

        (lexeme, file, line, column) = self.token
        ns = Scope(scope)
        self.define(ns, self.args)
        R = ("result", file, line, column)
        ns.names["result"] = ("local-var", R)
        if self.atomically:
            code.append(AtomicIncOp(True))
        self.stat.compile(ns, code)
        if self.atomically:
            code.append(AtomicDecOp())
        code.append(StoreVarOp(R))
        code.append(ReturnOp())
        code.nextLabel(endlabel)
        return startlabel

    def compile(self, scope, code):
        startlabel = self.compile_body(scope, code)
        (lexeme, file, line, column) = self.token
        code.append(PushOp((startlabel, file, line, column)))

class CallAST(AST):
    def __init__(self, token, atomically, expr):
        AST.__init__(self, token, atomically)
        self.expr = expr

    def __repr__(self):
        return "Call(" + str(self.expr) + ")"

    def compile(self, scope, code):
        if not self.expr.isConstant(scope):
            if self.atomically:
                code.append(AtomicIncOp(True))
            self.expr.compile(scope, code)
            if self.atomically:
                code.append(AtomicDecOp())
            code.append(PopOp())

class SpawnAST(AST):
    def __init__(self, token, atomically, method, arg, this, eternal):
        AST.__init__(self, token, atomically)
        self.method = method
        self.arg = arg
        self.this = this
        self.eternal = eternal

    def __repr__(self):
        return "Spawn(" + str(self.method) + ", " + str(self.arg) + ", "  + str(self.this) + ", " + str(self.eternal) + ")"

    def compile(self, scope, code):
        self.method.compile(scope, code)
        self.arg.compile(scope, code)
        if self.this == None:
            code.append(PushOp((novalue, None, None, None)))
        else:
            self.this.compile(scope, code)
        code.append(SpawnOp(self.eternal))

class TrapAST(AST):
    def __init__(self, token, atomically, method, arg):
        AST.__init__(self, token, atomically)
        self.method = method
        self.arg = arg

    def __repr__(self):
        return "Trap(" + str(self.method) + ", " + str(self.arg) + ")"

    def compile(self, scope, code):
        # TODO.  These should be swapped
        self.arg.compile(scope, code)
        self.method.compile(scope, code)
        code.append(TrapOp())

class GoAST(AST):
    def __init__(self, token, atomically, ctx, result):
        AST.__init__(self, token, atomically)
        self.ctx = ctx
        self.result = result

    def __repr__(self):
        return "Go(" + str(self.tag) + ", " + str(self.ctx) + ", " + str(self.result) + ")"

    # TODO.  Seems like context and argument are not evaluated in left to
    #        right order
    def compile(self, scope, code):
        if self.atomically:
            code.append(AtomicIncOp(True))
        self.result.compile(scope, code)
        self.ctx.compile(scope, code)
        if self.atomically:
            code.append(AtomicDecOp())
        code.append(GoOp())

class ImportAST(AST):
    def __init__(self, token, atomically, modlist):
        AST.__init__(self, token, atomically)
        self.modlist = modlist

    def __repr__(self):
        return "Import(" + str(self.modlist) + ")"

    def compile(self, scope, code):
        for module in self.modlist:
            self.doImport(scope, code, module)

    def getImports(self):
        return self.modlist

class FromAST(AST):
    def __init__(self, token, atomically, module, items):
        AST.__init__(self, token, atomically)
        self.module = module
        self.items = items

    def __repr__(self):
        return "FromImport(" + str(self.module) + ", " + str(self.items) + ")"

    def compile(self, scope, code):
        self.doImport(scope, code, self.module)
        (lexeme, file, line, column) = self.module
        names = imported[lexeme].names
        # TODO.  Check for overlap, existence, etc.
        if self.items == []:  # from module import *
            for (item, (t, v)) in names.items():
                if t == "constant":
                    scope.names[item] = (t, v)
        else:
            for (lexeme, file, line, column) in self.items:
                if lexeme not in names:
                    raise HarmonyCompilerError(
                        filename=file,
                        lexeme=lexeme,
                        message="%s line %s: can't import %s from %s" % (file, line, lexeme, self.module[0]),
                        line=line, column=column)
                (t, v) = names[lexeme]
                assert t == "constant", (lexeme, t, v)
                scope.names[lexeme] = (t, v)

    def getImports(self):
        return [self.module]

class LocationAST(AST):
    def __init__(self, token, ast, file, line):
        AST.__init__(self, token, True)
        self.ast = ast
        self.file = file
        self.line = line

    def __repr__(self):
        return "LocationAST(" + str(self.ast) + ")"

    def compile(self, scope, code):
        code.location(self.file, self.line)
        self.ast.compile(scope, code)

    def getLabels(self):
        return self.ast.getLabels()

    def getImports(self):
        return self.ast.getImports()

class LabelStatAST(AST):
    def __init__(self, token, labels, ast):
        AST.__init__(self, token, True)
        self.labels = { lb:LabelValue(None, "label") for lb in labels }
        self.ast = ast

    def __repr__(self):
        return "LabelStatAST(" + str(self.labels) + ", " + str(self.ast) + ")"

    # TODO.  Update label stuff
    def compile(self, scope, code):
        # root = scope
        # while root.parent != None:
        #     root = root.parent
        for ((lexeme, file, line, column), label) in self.labels.items():
            code.nextLabel(label)
            # root.names[lexeme] = ("constant", (label, file, line, column))
        code.append(AtomicIncOp(False))
        self.ast.compile(scope, code)
        code.append(AtomicDecOp())

    def getLabels(self):
        return set(self.labels.items()) | self.ast.getLabels()

    def getImports(self):
        return self.ast.getImports()

class SequentialAST(AST):
    def __init__(self, token, atomically, vars):
        AST.__init__(self, token, atomically)
        self.vars = vars
    
    def __repr__(self):
        return "Sequential(" + str(self.vars) + ")"

    def compile(self, scope, code):
        for lv in self.vars:
            lv.ph1(scope, code)
            code.append(SequentialOp())

class ConstAST(AST):
    def __init__(self, token, atomically, const, expr):
        AST.__init__(self, token, atomically)
        self.const = const
        self.expr = expr

    def __repr__(self):
        return "Const(" + str(self.const) + ", " + str(self.expr) + ")"

    def set(self, scope, const, v):
        if isinstance(const, tuple):
            (lexeme, file, line, column) = const
            if lexeme in constants:
                value = constants[lexeme]
                used_constants.add(lexeme)
            else:
                value = v
            scope.names[lexeme] = ("constant", (value, file, line, column))
        else:
            assert isinstance(const, list), const
            assert isinstance(v, DictValue), v
            assert len(const) == len(v.d), (const, v)
            for i in range(len(const)):
                self.set(scope, const[i], v.d[i])

    def compile(self, scope, code):
        if not self.expr.isConstant(scope):
            lexeme, file, line, column = self.expr.ast_token if isinstance(self.expr, AST) else self.ast_token
            raise HarmonyCompilerError(
                filename=file,
                lexeme=lexeme,
                line=line,
                column=column,
                message="%s: Parse error: expression not a constant %s" % (self.const, self.expr),
            )
        if isinstance(self.expr, LambdaAST):
            pc = self.expr.compile_body(scope, code)
            self.set(scope, self.const, PcValue(pc))
        else:
            code2 = Code()
            self.expr.compile(scope, code2)
            state = State(code2, scope.labels)
            ctx = ContextValue(("__const__", None, None, None), 0, novalue, novalue)
            ctx.atomic = 1
            while ctx.pc != len(code2.labeled_ops):
                code2.labeled_ops[ctx.pc].op.eval(state, ctx)
            v = ctx.pop()
            self.set(scope, self.const, v)

class StatListRule(Rule):
    def __init__(self, indent, atomically):
        self.indent = indent
        self.atomically = atomically

    def parse(self, t):
        if t == []:
            raise HarmonyCompilerError(
                message='Unexpected EOF',
                is_eof_error=True
            )

        # find all the tokens that are indented more than self.indent
        slice = []
        first_token = t[0]
        (lexeme, file, line, column) = t[0]
        while column > self.indent:
            slice.append(t[0])
            t = t[1:]
            if t == []:
                break
            (lexeme, file, line, column) = t[0]
        if slice == []:
            raise HarmonyCompilerError(
                filename=file,
                lexeme=lexeme,
                line=line,
                column=column,
                message="Parse error: no statements in indented block: %s" % str(t[0]),
            )

        b = []
        while slice != []:
            try:
                (lexeme, thefile, theline, column) = token = slice[0]
                (ast, slice) = StatementRule().parse(slice)
                b.append(LocationAST(token, ast, thefile, theline))
            except IndexError:
                lexeme, file, line, column = slice[0]
                raise HarmonyCompilerError(
                    filename=file,
                    lexeme=lexeme,
                    line=line,
                    column=column,
                    message="Parsing: incomplete statement starting at %s" % str(slice[0]),
                )

        return (BlockAST(first_token, self.atomically, b), t)

class BlockRule(Rule):
    def __init__(self, indent, atomically):
        self.indent = indent
        self.atomically = atomically

    def parse(self, t):
        (lexeme, file, line, column) = t[0]
        self.expect("block statement", lexeme == ":", t[0], "missing ':'")
        return StatListRule(self.indent, self.atomically).parse(t[1:])

# This parses the lefthand side of an assignment in a let expression.  Grammar:
#   lhs = (tuple ",")* [tuple]
#   tuple = name | "(" lhs ")"
# TODO: also use this for def arguments and for
class BoundVarRule(Rule):
    def parse(self, t):
        tuples = []
        while True:
            (lexeme, file, line, column) = t[0]
            if (isname(lexeme)):
                tuples.append(t[0])
            elif lexeme == "(":
                (nest, t) = BoundVarRule().parse(t[1:])
                (lexeme, file, line, column) = t[0]
                self.expect("let statement", lexeme == ")", t[0], "expected ')'")
                tuples.append(nest)
            elif lexeme == "[":
                (nest, t) = BoundVarRule().parse(t[1:])
                (lexeme, file, line, column) = t[0]
                self.expect("let statement", lexeme == "]", t[0], "expected ']'")
                tuples.append(nest)
            else:
                return (tuples, t)
            (lexeme, file, line, column) = t[1]
            if lexeme != ",":
                if len(tuples) == 1:
                    return (tuples[0], t[1:])
                else:
                    return (tuples, t[1:])
            t = t[2:]

class StatementRule(Rule):
    def rec_slice(self, t):
        (lexeme, file, line, column) = first = t[0]
        if lexeme == '(':
            bracket = ')'
        elif lexeme == '[':
            bracket = ']'
        else:
            assert lexeme == '{'
            bracket = '}'
        t = t[1:]
        tokens = []
        while t != []:
            tokens.append(t[0])
            (lexeme, file, line, column) = t[0]
            if lexeme == bracket:
                return (tokens, t[1:])
            if lexeme in [')', ']', '}']:
                raise HarmonyCompilerError(
                    filename=file,
                    lexeme=lexeme,
                    line=line,
                    column=column,
                    message="unmatched bracket: %s" % str(t[0]),
                )
            if lexeme in ['(', '[', '{']:
                (more, t) = self.rec_slice(t)
                tokens += more
                if t == []:
                    break
            else:
                t = t[1:]
        raise HarmonyCompilerError(
            filename=file,
            lexeme=lexeme,
            line=line,
            column=column,
            message="closing bracket missing: %s %s %s" % (first, tokens, t),
        )

    def slice(self, t, indent):
        if t == []:
            return ([], [])
        tokens = []
        (lexeme, file, line, column) = t[0]
        if lexeme in ['(', '[', '{']:
            tokens.append(t[0])
            (more, t) = self.rec_slice(t)
            tokens += more
            if t == []:
                return (tokens, [])
            (lexeme, file, line, column) = t[0]
        while column > indent and lexeme != ";":
            tokens.append(t[0])
            t = t[1:]
            if t == []:
                break
            (lexeme, file, line, column) = t[0]
            if lexeme in ['(', '[', '{']:
                tokens.append(t[0])
                (more, t) = self.rec_slice(t)
                tokens += more
                if t == []:
                    break
                (lexeme, file, line, column) = t[0]
        return (tokens, t)

    def parse(self, t):
        (lexeme, file, line, column) = t[0]
        if lexeme == ";":
            return (PassAST(t[0], False), t[1:])
        if lexeme == "atomically":
            atomically = True
            t = t[1:]
            (lexeme, _, _, _) = t[0]
        else:
            atomically = False
        token = t[0]
        if lexeme == ":":
            return BlockRule(column, atomically).parse(t)
        if isname(lexeme) and t[1][0] == ":":
            (lexeme, file, line, nextColumn) = token
            (stat, t) = BlockRule(column, False).parse(t[1:])
            return (LabelStatAST(token, [token], stat), t)
        if lexeme == "const":
            (tokens, t) = self.slice(t[1:], column)
            (const, tokens) = BoundVarRule().parse(tokens)
            (lexeme, file, line, column) = tokens[0]
            self.expect("constant definition", lexeme == "=", tokens[0], "expected '='")
            (ast, tokens) = TupleRule(set()).parse(tokens[1:])
            if tokens != []:
                lexeme, file, line, column = tokens[0]
                raise HarmonyCompilerError(
                    filename=file,
                    lexeme=lexeme,
                    line=line,
                    column=column,
                    message="constant definition: unexpected token: %s" % str(tokens[0]),
                )
            return (ConstAST(token, atomically, const, ast), t)
        if lexeme == "if":
            alts = []
            while True:
                (cond, t) = NaryRule({":"}).parse(t[1:])
                (stat, t) = StatListRule(column, False).parse(t[1:])
                alts += [(cond, stat, file, line)]
                if t == []:
                    nextColumn = column
                    break
                (lexeme, file, line, nextColumn) = t[0]
                assert nextColumn <= column
                if nextColumn < column:
                    break
                if lexeme != "elif":
                    break
            if nextColumn == column and lexeme == "else":
                (stat, t) = BlockRule(column, False).parse(t[1:])
            else:
                stat = None
            return (IfAST(token, atomically, alts, stat), t)
        if lexeme == "while":
            (cond, t) = NaryRule({":"}).parse(t[1:])
            (stat, t) = StatListRule(column, False).parse(t[1:])
            return (WhileAST(token, atomically, cond, stat), t)
        if lexeme == "await":
            (tokens, t) = self.slice(t[1:], column)
            (cond, tokens) = NaryRule(set()).parse(tokens)
            if tokens != []:
                lexeme, file, line, column = tokens[0]
                raise HarmonyCompilerError(
                    filename=file,
                    lexeme=lexeme,
                    line=line,
                    column=column,
                    message="await: unexpected token: %s" % str(tokens[0]),
                )
            return (LetWhenAST(token, atomically, [ ('cond', cond) ], PassAST(token, False)), t)
        if lexeme == "invariant":
            (tokens, t) = self.slice(t[1:], column)
            (cond, tokens) = NaryRule(set()).parse(tokens)
            if tokens != []:
                lexeme, file, line, column = tokens[0]
                raise HarmonyCompilerError(
                    filename=file,
                    lexeme=lexeme,
                    line=line,
                    column=column,
                    message="invariant: unexpected token: %s" % str(tokens[0]),
                )
            return (InvariantAST(cond, token, atomically), t)
        if lexeme == "for":
            (lst, t) = self.iterParse(t[1:], {":"})
            (stat, t) = StatListRule(column, False).parse(t[1:])
            return (ForAST(lst, stat, token, atomically), t)

        if lexeme in { "let", "when" }:
            vars_and_conds = []
            while lexeme != ':':
                if lexeme == "let":
                    (bv, t) = BoundVarRule().parse(t[1:])
                    (lexeme, file, line, nextColumn) = t[0]
                    self.expect("let statement", lexeme == "=", t[0], "expected '='")
                    (ast, t) = TupleRule({":", "let", "when"}).parse(t[1:])
                    vars_and_conds.append(('var', bv, ast))
                else:
                    assert lexeme == "when"
                    (lexeme, file, line, nextColumn) = t[1]
                    if lexeme == "exists":
                        (bv, t) = BoundVarRule().parse(t[2:])
                        (lexeme, file, line, nextColumn) = t[0]
                        self.expect("'when exists' statement", lexeme == "in", t[0], "expected 'in'")
                        (expr, t) = NaryRule({":", "let", "when"}).parse(t[1:])
                        (lexeme, file, line, nextColumn) = t[0]
                        vars_and_conds.append(('exists', bv, expr))
                    else:
                        (cond, t) = NaryRule({":", "let", "when"}).parse(t[1:])
                        vars_and_conds.append(('cond', cond))
                (lexeme, file, line, nextColumn) = t[0]

            (stat, t) = StatListRule(column, False).parse(t[1:])

            if all(vac[0] == 'var' for vac in vars_and_conds):
                vars = [vac[1:] for vac in vars_and_conds if vac[0] == 'var']
                return (LetAST(token, atomically, vars, stat), t)

            else:
                return (LetWhenAST(token, atomically, vars_and_conds, stat), t)

        if lexeme == "var":
            vars = []
            (bv, t) = BoundVarRule().parse(t[1:])
            (lexeme, file, line, nextColumn) = t[0]
            self.expect("var statement", lexeme == "=", t[0], "expected '='")
            t = t[1:]

            same_line = []
            for tok in t:
                if tok[2] != line:
                    break
                same_line.append(tok)

            t = t[len(same_line):]
            (ast, u) = TupleRule(set()).parse(same_line)
            self.expect(
                "var statement",
                len(u) == 0,
                'remaining tokens on line %d: %s'%(line, u),
                'no remaining tokens'
            )
            vars.append((bv, ast))
            return (VarAST(token, atomically, vars), t)

        if lexeme == "del":
            (tokens, t) = self.slice(t[1:], column)
            (ast, tokens) = ExpressionRule().parse(tokens)
            if tokens != []:
                lexeme, file, line, column = tokens[0]
                raise HarmonyCompilerError(
                    filename=file,
                    lexeme=lexeme,
                    line=line,
                    column=column,
                    message="del: unexpected token: %s" % str(tokens[0]),
                )
            return (DelAST(token, atomically, ast), t)
        if lexeme == "def":
            name = t[1]
            (lexeme, file, line, nextColumn) = name
            self.expect("method definition", isname(lexeme), name, "expected name")
            (bv, t) = BoundVarRule().parse(t[2:])
            (stat, t) = BlockRule(column, False).parse(t)
            return (MethodAST(token, atomically, name, bv, stat), t)
        if lexeme == "spawn":
            (tokens, t) = self.slice(t[1:], column)
            (lexeme, file, line, col) = tokens[0]
            if lexeme == "eternal":
                tokens = tokens[1:]
                eternal = True
            else:
                eternal = False
            (func, tokens) = NaryRule({","}).parse(tokens)
            if not isinstance(func, ApplyAST):
                token = func.ast_token if isinstance(func, AST) else tokens[0] if tokens else token
                lexeme, file, line, column = token
                raise HarmonyCompilerError(
                    filename=file,
                    lexeme=lexeme,
                    line=line,
                    column=column,
                    message="spawn: expected method application %s" % str(token),
                )
            if tokens == []:
                this = None
            else:
                (lexeme, file, line, column) = tokens[0]
                assert lexeme == ","
                (this, tokens) = NaryRule(set()).parse(tokens[1:])
                if tokens != []:
                    lexeme, file, line, column = tokens[0]
                    raise HarmonyCompilerError(
                        filename=file,
                        lexeme=lexeme,
                        line=line,
                        column=column,
                        message="spawn: unexpected token: %s" % str(tokens[0]),
                    )
            return (SpawnAST(token, atomically, func.method, func.arg, this, eternal), t)
        if lexeme == "trap":
            (tokens, t) = self.slice(t[1:], column)
            (func, tokens) = NaryRule(set()).parse(tokens)
            if not isinstance(func, ApplyAST):
                token = func.ast_token if isinstance(func, AST) else tokens[0] if tokens else token
                lexeme, file, line, column = token
                raise HarmonyCompilerError(
                    filename=file,
                    lexeme=lexeme,
                    line=line,
                    column=column,
                    message="trap: expected method application: %s" % str(token),
                )
            if tokens != []:
                lexeme, file, line, column = tokens[0]
                raise HarmonyCompilerError(
                    filename=file,
                    lexeme=lexeme,
                    line=line,
                    column=column,
                    message="trap: unexpected token: %s" % str(tokens[0]),
                )
            return (TrapAST(token, atomically, func.method, func.arg), t)
        if lexeme == "go":
            (tokens, t) = self.slice(t[1:], column)
            (func, tokens) = NaryRule(set()).parse(tokens)
            if not isinstance(func, ApplyAST):
                token = func.ast_token if isinstance(func, AST) else tokens[0] if tokens else token
                lexeme, file, line, column = token
                raise HarmonyCompilerError(
                    filename=file,
                    lexeme=lexeme,
                    line=line,
                    column=column,
                    message="go: expected method application: %s" % str(token),
                )
            if tokens != []:
                lexeme, file, line, column = tokens[0]
                raise HarmonyCompilerError(
                    filename=file,
                    lexeme=lexeme,
                    line=line,
                    column=column,
                    message="go: unexpected token: %s" % str(tokens[0]),
                )
            return (GoAST(token, atomically, func.method, func.arg), t)
        if lexeme == "pass":
            return (PassAST(token, atomically), t[1:])
        if lexeme == "sequential":
            (tokens, t) = self.slice(t[1:], column)
            (ast, tokens) = ExpressionRule().parse(tokens)
            vars = [ast]
            if tokens != []:
                (lexeme, file, line, column) = tokens[0]
                while lexeme == ',':
                    (ast, tokens) = ExpressionRule().parse(tokens[1:])
                    vars.append(ast)
                    if tokens == []:
                        break
                    (lexeme, file, line, column) = tokens[0]
                if tokens != []:
                    lexeme, file, line, column = tokens[0]
                    raise HarmonyCompilerError(
                        filename=file,
                        lexeme=lexeme,
                        line=line,
                        column=column,
                        message="sequential: unexpected token: %s" % str(tokens[0]),
                    )
            return (SequentialAST(token, atomically, vars), t)
        if lexeme == "import":
            (tokens, t) = self.slice(t[1:], column)
            mods = [tokens[0]]
            tokens = tokens[1:]
            if tokens != []:
                (lexeme, file, line, column) = tokens[0]
                while lexeme == ',':
                    mods.append(tokens[1])
                    tokens = tokens[2:]
                    if tokens == []:
                        break
                    (lexeme, file, line, column) = tokens[0]
                if tokens != []:
                    lexeme, file, line, column = tokens[0]
                    raise HarmonyCompilerError(
                        filename=file,
                        lexeme=lexeme,
                        line=line,
                        column=column,
                        message="import: unexpected token: %s" % str(tokens[0]),
                    )

            return (ImportAST(token, atomically, mods), t)
        if lexeme == "from":
            (tokens, t) = self.slice(t[1:], column)
            (lexeme, file, line, column) = module = tokens[0]
            self.expect("from statement", isname(lexeme), module, "expected module name")
            (lexeme, file, line, column) = tokens[1]
            self.expect("from statement", lexeme == "import", tokens[1], "expected 'import'")
            (lexeme, file, line, column) = tokens[2]
            if lexeme == '*':
                assert len(tokens) == 3, tokens
                return (FromAST(token, atomically, module, []), t)
            items = [tokens[2]]
            tokens = tokens[3:]
            if tokens != []:
                (lexeme, file, line, column) = tokens[0]
                while lexeme == ',':
                    items.append(tokens[1])
                    tokens = tokens[2:]
                    if tokens == []:
                        break
                    (lexeme, file, line, column) = tokens[0]
            if tokens != []:
                lexeme, file, line, column = tokens[0]
                raise HarmonyCompilerError(
                    filename=file,
                    lexeme=lexeme,
                    line=line,
                    column=column,
                    message="from: unexpected token: %s" % str(tokens[0]),
                )

            return (FromAST(token, atomically, module, items), t)
        if lexeme == "assert":
            (tokens, t) = self.slice(t[1:], column)
            (cond, tokens) = NaryRule({","}).parse(tokens)
            if tokens == []:
                expr = None
            else:
                (lexeme, file, line, column) = tokens[0]
                if lexeme != ",":
                    raise HarmonyCompilerError(
                        filename=file,
                        lexeme=lexeme,
                        line=line,
                        column=column,
                        message="assert: unexpected token: %s" % str(tokens[0]),
                    )
                (expr, tokens) = NaryRule(set()).parse(tokens[1:])
                if tokens != []:
                    lexeme, file, line, column = tokens[0]
                    raise HarmonyCompilerError(
                        filename=file,
                        lexeme=lexeme,
                        line=line,
                        column=column,
                        message="assert: unexpected token: %s" % str(tokens[0]),
                    )
            return (AssertAST(token, atomically, cond, expr), t)
        if lexeme == "print":
            (tokens, t) = self.slice(t[1:], column)
            (cond, tokens) = NaryRule(set()).parse(tokens)
            if tokens != []:
                lexeme, file, line, column = tokens[0]
                raise HarmonyCompilerError(
                    filename=file,
                    lexeme=lexeme,
                    line=line,
                    column=column,
                    message="print: unexpected token: %s" % str(tokens[0]),
                )
            return (PrintAST(token, atomically, cond), t)
        if lexeme == "possibly":
            (tokens, t) = self.slice(t[1:], column)
            (cond, tokens) = NaryRule({","}).parse(tokens)
            condlist = [ cond ]
            while tokens != []:
                (lexeme, file, line, column) = tokens[0]
                if lexeme != ",":
                    raise HarmonyCompilerError(
                        filename=file,
                        lexeme=lexeme,
                        line=line,
                        column=column,
                        message="possibly: unexpected token: %s" % str(tokens[0]),
                    )
                (cond, tokens) = NaryRule({","}).parse(tokens[1:])
                condlist.append(cond)
            return (PossiblyAST(token, atomically, condlist), t)
        
        # If we get here, the next statement is either an expression
        # or an assignment.  The assignment grammar is either
        #   (tuple_expression '=')* tuple_expression
        # or
        #   tuple_expression 'op=' tuple_expression
        (lexeme, file, line, column) = t[0]
        if lexeme in ['(', '[', '{']:
            (tokens, t) = self.slice(t, column)
        else:
            (tokens, t) = self.slice(t[1:], column)
            tokens = [token] + tokens
        exprs = []
        assignop = None
        while tokens != []:
            tk = tokens[0]
            (ast, tokens) = TupleRule({ "=" } | assignops).parse(tokens)
            self.expect("statement", ast != False, tk, "expected expression")
            exprs.append(ast)
            if tokens == []:
                break
            (lexeme, file, line, column) = tokens[0]
            assert assignop == None or assignop[0] == "="
            assignop = tokens[0]
            tokens = tokens[1:]
        if len(exprs) == 1:
            return (CallAST(token, atomically, exprs[0]), t)
        else:
            return (AssignmentAST(exprs[:-1], exprs[-1], assignop, atomically), t)

class ContextValue(Value):
    def __init__(self, name, entry, arg, this):
        self.name = name
        self.entry = entry
        self.arg = arg
        self.pc = entry
        self.this = this
        self.atomic = 0
        self.readonly = 0
        self.interruptLevel = False
        self.stack = []     # collections.deque() seems slightly slower
        self.fp = 0         # frame pointer
        self.vars = novalue
        self.trap = None
        self.phase = "start"        # start, middle, or end
        self.stopped = False
        self.failure = None

    def __repr__(self):
        return "ContextValue(" + str(self.name) + ", " + str(self.arg) + ", " + str(self.this) + ")"

    def __str__(self):
        return self.__repr__()

    def nametag(self):
        if self.arg == novalue:
            return self.name[0] + "()"
        return self.name[0] + "(" + str(self.arg) + ")"

    def __hash__(self):
        h = (self.name, self.entry, self.arg, self.pc, self.this, self.atomic, self.readonly, self.interruptLevel, self.vars,
            self.trap, self.phase, self.stopped, self.failure).__hash__()
        for v in self.stack:
            h ^= v.__hash__()
        return h

    def __eq__(self, other):
        if not isinstance(other, ContextValue):
            return False
        if self.name != other.name:
            return False
        if self.entry != other.entry:
            return False
        if self.arg != other.arg:
            return False
        if self.pc != other.pc:
            return False
        if self.this != other.this:
            return False
        if self.atomic != other.atomic:
            return False
        if self.readonly != other.readonly:
            return False
        if self.interruptLevel != other.interruptLevel:
            return False
        if self.phase != other.phase:
            return False
        if self.stopped != other.stopped:
            return False
        if self.fp != other.fp:
            return False
        if self.trap != other.trap:
            return False
        if self.failure != other.failure:
            return False
        return self.stack == other.stack and self.vars == other.vars

    def copy(self):
        c = ContextValue(self.name, self.entry, self.arg, self.this)
        c.pc = self.pc
        c.atomic = self.atomic
        c.readonly = self.readonly
        c.interruptLevel = self.interruptLevel
        c.stack = self.stack.copy()
        c.fp = self.fp
        c.trap = self.trap
        c.vars = self.vars
        c.phase = self.phase
        c.stopped = self.stopped
        c.failure = self.failure
        return c

    def get(self, var):
        return self.this if var == "this" else self.vars.d[var]

    def iget(self, indexes):
        assert indexes[0] != "this"
        v = self.vars
        while indexes != []:
            v = v.d[indexes[0]]
            indexes = indexes[1:]
        return v

    def update(self, record, indexes, val):
        if len(indexes) > 1:
            v = self.update(record.d[indexes[0]], indexes[1:], val)
        else:
            v = val
        d = record.d.copy()
        d[indexes[0]] = v
        return DictValue(d)

    def doDelete(self, record, indexes):
        if len(indexes) > 1:
            d = record.d.copy()
            d[indexes[0]] = self.doDelete(record.d[indexes[0]], indexes[1:])
        else:
            d = record.d.copy()
            if indexes[0] in d:
                del d[indexes[0]]
        return DictValue(d)

    def set(self, indexes, val):
        if indexes[0] == "this":
            if len(indexes) == 1:
                self.this = val
            else:
                self.this = self.update(self.this, indexes[1:], val)
        else:
            self.vars = self.update(self.vars, indexes, val)

    def delete(self, indexes):
        self.vars = self.doDelete(self.vars, indexes)

    def push(self, val):
        assert val != None
        self.stack.append(val)

    def pop(self):
        return self.stack.pop()

    def key(self):
        return (100, (self.pc, self.__hash__()))

class State:
    def __init__(self, code, labels):
        self.code = code
        self.labels = labels
        self.vars = novalue
        self.ctxbag = {}        # running contexts
        self.stopbag = {}       # stopped contexts
        self.termbag = {}       # terminated contexts
        self.choosing = None
        self.invariants = set()
        self.initializing = True

    def __repr__(self):
        return "State(" + str(self.vars) + ", " + str(self.ctxbag) + ", " + \
            str(self.stopbag) + ", " + str(self.invariants) + ")"

    def __hash__(self):
        h = self.vars.__hash__()
        for c in self.ctxbag.items():
            h ^= c.__hash__()
        for c in self.stopbag.items():
            h ^= c.__hash__()
        for c in self.termbag.items():
            h ^= c.__hash__()
        for i in self.invariants:
            h ^= i
        return h

    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        assert self.code == other.code and self.labels == other.labels
        if self.vars != other.vars:
            return False
        if self.ctxbag != other.ctxbag:
            return False
        if self.stopbag != other.stopbag:
            return False
        if self.termbag != other.termbag:
            return False
        if self.choosing != other.choosing:
            return False
        if self.invariants != other.invariants:
            return False
        if self.initializing != self.initializing:
            return False
        return True

    def copy(self):
        s = State(self.code, self.labels)
        s.vars = self.vars      # no need to copy as store operations do it
        s.ctxbag = self.ctxbag.copy()
        s.stopbag = self.stopbag.copy()
        s.termbag = self.termbag.copy()
        s.choosing = self.choosing
        s.invariants = self.invariants.copy()
        s.initializing = self.initializing
        return s

    def get(self, var):
        return self.vars.d[var]

    def iget(self, indexes):
        path = indexes
        v = self.vars
        while indexes != []:
            try:
                v = v.d[indexes[0]]
            except KeyError:
                print()
                print("no index", indexes[0], "in variable", path)
                sys.exit(1)
            indexes = indexes[1:]
        return v

    def update(self, record, indexes, val):
        if len(indexes) > 1:
            v = self.update(record.d[indexes[0]], indexes[1:], val)
        else:
            v = val
        d = record.d.copy()
        d[indexes[0]] = v
        return DictValue(d)

    def doDelete(self, record, indexes):
        d = record.d.copy()
        if len(indexes) > 1:
            d[indexes[0]] = self.doDelete(record.d[indexes[0]], indexes[1:])
        else:
            del d[indexes[0]]
        return DictValue(d)

    def doStop(self, record, indexes, ctx):
        d = record.d.copy()
        if len(indexes) > 1:
            d[indexes[0]] = self.doStop(record.d[indexes[0]], indexes[1:], ctx)
        else:
            # TODO.  Should be print + set failure
            list = d[indexes[0]]
            assert(isinstance(list, DictValue))
            d2 = list.d.copy()
            d2[len(d2)] = ctx
            d[indexes[0]] = DictValue(d2)
        return DictValue(d)

    def set(self, indexes, val):
        self.vars = self.update(self.vars, indexes, val)

    def delete(self, indexes):
        self.vars = self.doDelete(self.vars, indexes)

    def stop(self, indexes, ctx):
        self.vars = self.doStop(self.vars, indexes, ctx)
        cnt = self.stopbag.get(ctx)
        if cnt == None:
            self.stopbag[ctx] = 1
        else:
            self.stopbag[ctx] = cnt + 1

class Node:
    def __init__(self, state, uid, parent, before, after, steps, len):
        self.state = state      # State associated with this node
        self.uid = uid          # index into 'nodes' array
        self.parent = parent    # next hop on way to initial state
        self.len = len          # length of path to initial state
        self.before = before    # the context that made the hop from the parent state
        self.after = after      # the resulting context
        self.steps = steps      # list of microsteps

        # if state.choosing, maps choice, else context
        self.edges = {}         # map to <nextNode, nextContext, steps>

        self.sources = set()    # backward edges
        self.expanded = False   # lazy deletion
        self.issues = set()     # set of problems with this state
        self.cid = 0            # strongly connected component id
        self.blocked = {}       # map of context -> boolean

    def __hash__(self):
        return self.uid

    def __eq__(self, other):
        return isinstance(other, Node) and other.uid == self.uid

    def rec_isblocked(self, ctx, vars, seen):
        if self.uid in seen:
            return True
        seen.add(self.uid)
        if ctx in self.blocked:
            return self.blocked[ctx]
        s = self.state
        if s.choosing == ctx:
            for (choice, next) in self.edges.items():
                (nn, nc, steps) = next
                ns = nn.state
                if ns.vars != vars or not nn.rec_isblocked(nc, vars, seen):
                    self.blocked[ctx] = False
                    return False
        elif ctx in self.edges:
            next = self.edges[ctx]
            (nn, nc, steps) = next
            ns = nn.state
            if ns.vars != vars or not nn.rec_isblocked(nc, vars, seen):
                self.blocked[ctx] = False
                return False
        else:
            self.blocked[ctx] = False
            return False
        self.blocked[ctx] = True
        return True

    # See if the given process is "blocked", i.e., it cannot change
    # the shared state (the state variables), terminate, or stop unless
    # some other process changes the shared state first
    def isblocked(self, ctx):
        return self.rec_isblocked(ctx, self.state.vars, set())

def strsteps(steps):
    if steps == None:
        return "[]"
    result = ""
    i = 0
    while i < len(steps):
        if result != "":
            result += ","
        (pc, choice) = steps[i]
        if pc == None:
            result += "Interrupt"
        else:
            result += str(pc)
        j = i + 1
        if choice != None:
            result += "(choose %s)"%strValue(choice)
        else:
            while j < len(steps):
                (pc2, choice2) = steps[j]
                if pc == None or pc2 != pc + 1 or choice2 != None:
                    break
                (pc, choice) = (pc2, choice2)
                j += 1
            if j > i + 1:
                result += "-%d"%pc
        i = j
    return "[" + result + "]"

def find_shortest(bad):
    best_node = None
    best_len = 0
    for node in bad:
        if best_node == None or node.len < best_len:
            best_node = node
            best_len = node.len
    return best_node

def varvisit(d, vars, name, r):
    if isinstance(d, dict):
        for k in sorted(d.keys()):
            if isinstance(k, str):
                nn = name + "." + k
            else:
                nn = name + "[" + strValue(k) + "]"
            if k in vars.d:
                varvisit(d[k], vars.d[k], nn, r)
            else:
                r.append("%s: ---"%nn)
    else:
        r.append("%s: %s"%(name, strValue(vars)))

def strvars(d, vars):
    r = []
    for k in sorted(d.keys()):
        varvisit(d[k], vars.d[k], k, r)
    return "{ " + ", ".join(r) + " }"

def varmerge(d, vars):
    assert isinstance(d, dict)
    assert isinstance(vars, DictValue)
    for (k, v) in vars.d.items():
        if k in d and isinstance(d[k], dict) and isinstance(v, DictValue):
            varmerge(d[k], v)
        elif k not in d and isinstance(v, DictValue):
            d[k] = {}
            varmerge(d[k], v)
        elif k not in d:
            d[k] = {v}
        elif isinstance(d[k], set):
            d[k] |= {v}
        else:
            assert isinstance(d[k], dict)
            d[k] = { v }

def vartrim(d):
    pairs = list(d.items())
    for (k, v) in pairs:
        if v == {}:
            del d[k]
        elif isinstance(d[k], dict):
            vartrim(d[k])

def pathvars(path):
    d = {}
    for (fctx, ctx, steps, states, vars) in path:
        varmerge(d, vars)
    vartrim(d)
    return d

def print_path(bad_node):
    path = genpath(bad_node)
    d = pathvars(path)
    pids = []
    for (fctx, ctx, steps, states, vars) in path:
        try:
            pid = pids.index(fctx)
            pids[pid] = ctx
        except ValueError:
            pids.append(ctx)
            pid = len(pids) - 1
        print("T%d:"%pid, ctx.nametag(), strsteps(steps), ctx.pc, strvars(d, vars))
    if len(path) > 0:
        (fctx, ctx, steps, states, vars) = path[-1]
        if ctx.failure != None:
            print(">>>", ctx.failure)

class Scope:
    def __init__(self, parent):
        self.parent = parent               # parent scope
        self.names = { "this": ("local-var", ("this", "NOFILE", 0, 0)) }   # name to (type, x) map
        self.labels = {} if parent == None else parent.labels
        self.prefix = [] if parent == None else parent.prefix

    def copy(self):
        c = Scope(self.parent)
        c.names = self.names.copy()
        c.labels = self.labels.copy()
        c.prefix = self.prefix.copy()
        return c

    def checkUnused(self, name):
        (lexeme, file, line, column) = name
        tv = self.names.get(lexeme)
        if tv != None:
            (t, v) = tv
            assert t != "variable", ("variable name in use", name, v)

    def lookup(self, name):
        (lexeme, file, line, column) = name
        if lexeme == "_":
            return ("local-var", name)
        tv = self.names.get(lexeme)
        if tv != None:
            return tv
        ancestor = self.parent
        while ancestor != None:
            tv = ancestor.names.get(lexeme)
            if tv != None:
                # (t, v) = tv
                # if t == "local-var":
                #    return None
                return tv
            ancestor = ancestor.parent
        # print("Warning: unknown name:", name, " (assuming global variable)")
        self.names[lexeme] = ("global", name)
        return ("global", name)

def optjump(code, pc):
    while pc < len(code.labeled_ops):
        op = code.labeled_ops[pc].op
        if not isinstance(op, JumpOp):
            break
        pc = op.pc
    return pc

def optimize(code):
    for i in range(len(code.labeled_ops)):
        op = code.labeled_ops[i].op
        if isinstance(op, JumpOp):
            code.labeled_ops[i].op = JumpOp(optjump(code, op.pc))
        elif isinstance(op, JumpCondOp):
            code.labeled_ops[i].op = JumpCondOp(op.cond, optjump(code, op.pc))

def invcheck(state, inv):
    assert isinstance(state.code[inv], InvariantOp)
    op = state.code[inv]
    ctx = ContextValue(("__invariant__", None, None, None), 0, novalue, novalue)
    ctx.atomic = ctx.readonly = 1
    ctx.pc = inv + 1
    while ctx.pc != inv + op.cnt:
        old = ctx.pc
        state.code[ctx.pc].eval(state, ctx)
        assert ctx.pc != old, old
    assert len(ctx.stack) == 1
    assert isinstance(ctx.stack[0], bool)
    return ctx.stack[0]

class Pad:
    def __init__(self, descr):
        self.descr = descr
        self.value = ""
        self.lastlen = 0
    
    def __repr__(self):
        return self.descr + " = " + self.value

    def pad(self, v):
        if len(v) < len(self.value):
            self.value = " " * (len(self.value) - len(v))
        else:
            self.value = ""
        self.value += v

p_ctx = Pad("ctx")
p_pc  = Pad("pc")
p_ns  = Pad("#states")
p_dia = Pad("diameter")
p_ql  = Pad("#queue")

# Have context ctx make one (macro) step in the given state
def onestep(node, ctx, choice, interrupt, nodes, visited, todo):
    assert ctx.failure == None, ctx.failure

    # Keep track of whether this is the same context as the parent context
    samectx = ctx == node.after

    # Copy the state before modifying it
    sc = node.state.copy()   # sc is "state copy"
    sc.choosing = None

    # Make a copy of the context before modifying it (cc is "context copy")
    cc = ctx.copy()

    # Copy the choice as well
    choice_copy = choice

    steps = []

    if interrupt:
        assert not cc.interruptLevel
        (method, arg) = ctx.trap
        cc.push(PcValue(cc.pc))
        cc.push("interrupt")
        cc.push(arg)
        cc.pc = method.pc
        cc.trap = None
        cc.interruptLevel = True
        steps.append((None, None))      # indicates an interrupt

    localStates = set() # used to detect infinite loops
    loopcnt = 0         # only check for infinite loops after a while
    while cc.phase != "end":
        # execute one microstep
        steps.append((cc.pc, choice_copy))

        # print status update
        global lasttime, silent
        if not silent and time.time() - lasttime > 0.3:
            p_ctx.pad(cc.nametag())
            p_pc.pad(str(cc.pc))
            p_ns.pad(str(len(visited)))
            p_dia.pad(str(node.len))
            p_ql.pad(str(len(todo)))
            print(p_ctx, p_pc, p_ns, p_dia, p_ql, len(localStates), end="\r")
            lasttime = time.time()

        # If the current instruction is a "choose" instruction,
        # make the specified choice
        if isinstance(sc.code[cc.pc], ChooseOp):
            assert choice_copy != None
            cc.stack[-1] = choice_copy
            cc.pc += 1
            choice_copy = None
        else:
            assert choice_copy == None
            if type(sc.code[cc.pc]) in { LoadOp, StoreOp, AtomicIncOp }:
                assert cc.phase != "end"
                cc.phase = "middle"
            try:
                sc.code[cc.pc].eval(sc, cc)
            except Exception as e:
                traceback.print_exc()
                sys.exit(1)
                cc.failure = "Python assertion failed"

        if cc.failure != None or cc.stopped:
            break

        # See if this process is making a nondeterministic choice.
        # If so, we break out of the microstep loop.  However, only
        # this process is scheduled from this state.
        if isinstance(sc.code[cc.pc], ChooseOp):
            v = cc.stack[-1]
            if (not isinstance(v, SetValue)) or v.s == set():
                # TODO.  Need the location of the choose operation in the file
                cc.failure = "pc = " + str(cc.pc) + \
                    ": Error: choose can only be applied to non-empty sets"
                break

            # if there is only one choice, we can just keep on going
            if len(v.s) > 1:
                sc.choosing = cc
                break
            else:
                choice_copy = list(v.s)[0]

        # if we're about to access shared state, let other processes
        # go first assuming there are other processes and we're not
        # in "atomic" mode
        # TODO.  IS THIS CHECK RIGHT?
        if cc.phase != "start" and cc.atomic == 0 and type(sc.code[cc.pc]) in { LoadOp, StoreOp }: # TODO  and len(sc.ctxbag) > 1:
            break
        # TODO.  WHY NOT HAVE THE SAME CHECK HERE?
        if cc.phase != "start" and cc.atomic == 0 and type(sc.code[cc.pc]) in { AtomicIncOp }:
            break

        # ContinueOp always causes a break
        if isinstance(sc.code[cc.pc], ContinueOp):
            break

        # Detect infinite loops if there's a suspicion
        loopcnt += 1
        if loopcnt > 200:
            if (sc, cc) in localStates:
                cc.failure = "infinite loop"
                break
            localStates.add((sc.copy(), cc.copy()))

    # Remove original context from bag
    bag_remove(sc.ctxbag, ctx)

    # Put the resulting context into the bag unless it's done
    if cc.phase == "end":
        sc.initializing = False     # initializing ends when __init__ finishes
        bag_add(sc.termbag, cc)
    elif not cc.stopped:
        bag_add(sc.ctxbag, cc)

    length = node.len if samectx else (node.len + 1)
    next = visited.get(sc)
    if next == None:
        next = Node(sc, len(nodes), node, ctx, cc, steps, length)
        nodes.append(next)
        visited[sc] = next
        if samectx:
            todo.insert(0, next)
        else:
            todo.append(next)
    elif next.len > length:
        assert length == node.len and next.len == node.len + 1 and not next.expanded, (node.len, length, next.len, next.expanded)
        # assert not next.expanded, (node.len, length, next.len, next.expanded)
        next.len = length
        next.parent = node
        next.before = ctx
        next.after = cc
        next.steps = steps
        todo.insert(0, next)
    node.edges[choice if node.state.choosing else ctx] = (next, cc, steps)
    next.sources.add(node)
    if cc.failure != None:
        next.issues.add("Thread Failure")

def parseConstant(c, v):
    tokens = lexer(v, "<constant argument>")
    if tokens == []:
        raise HarmonyCompilerError(
            message="Empty constant"
        )
    try:
        (ast, rem) = ExpressionRule().parse(tokens)
    except IndexError:
        # best guess...
        raise HarmonyCompilerError(
            message="Parsing constant %s hit end of string" % str(v)
        )
    scope = Scope(None)
    code = Code()
    ast.compile(scope, code)
    state = State(code, scope.labels)
    ctx = ContextValue(("__arg__", None, None, None), 0, novalue, novalue)
    ctx.atomic = 1
    while ctx.pc != len(code.labeled_ops):
        code.labeled_ops[ctx.pc].op.eval(state, ctx)
    constants[c] = ctx.pop()

def doCompile(filenames, consts, mods, interface):
    for c in consts:
        try:
            i = c.index("=")
            parseConstant(c[0:i], c[i+1:])
        except (IndexError, ValueError):
            raise HarmonyCompilerError(
                message="Usage: -c C=V to define a constant"
            )

    global modules
    for m in mods:
        try:
            i = m.index("=")
            modules[m[0:i]] = m[i+1:]
        except (IndexError, ValueError):
            raise HarmonyCompilerError(
                message="Usage: -m module=version to specify a module version"
            )

    scope = Scope(None)
    code = Code()
    code.append(FrameOp(("__init__", None, None, None), []))
    for fname in filenames:
        try:
            with open(fname, encoding='utf-8') as fd:
                load(fd, fname, scope, code)
        except IOError:
            print("harmony: can't open", fname, file=sys.stderr)
            sys.exit(1)

    if interface != None:
        load_string("def __iface__(): result = (%s)"%interface,
            "interface", scope, code)

    code.append(ReturnOp())     # to terminate "__init__" process

    # Check for unused constants/modules
    unused_constant_def = constants.keys() - used_constants
    print(unused_constant_def)
    unused_module_def = modules.keys() - imported.keys()
    if len(unused_constant_def) > 0:
        raise HarmonyCompilerError(
            message="The following constants were defined from the command line but not used: " + ', '.join(unused_constant_def),
            filename=fname,
            line=0,
            column=0,
            lexeme="",
        )
    if len(unused_module_def) > 0:
        raise HarmonyCompilerError(
            message="The following modules were defined from the command line but not used: " + ', '.join(unused_module_def),
            filename=fname,
            line=0,
            column=0,
            lexeme="",
        )

    # Analyze liveness of variables
    newcode = code.liveness()

    newcode.link()
    optimize(newcode)
    return (newcode, scope)

def kosaraju1(nodes, stack):
    seen = set()
    for node in nodes:
        if node.uid in seen:
            continue
        seen.add(node.uid)
        S = [node]
        while S:
            u = S[-1]
            done = True
            for (nn, nc, steps) in u.edges.values():
                if nn.uid not in seen:
                    seen.add(nn.uid)
                    done = False
                    S.append(nn)
                    break
            if done:
                S.pop()
                stack.append(u)

def kosaraju2(nodes, node, seen, scc):
    stack2 = [node]
    while stack2 != []:
        node = stack2.pop()
        if node.uid in seen:
            continue
        seen.add(node.uid)
        node.cid = scc.cid
        scc.nodes.add(node)
        for nn in node.sources:
            if nn.uid not in seen:
                stack2.append(nn)

class SCC:
    def __init__(self, cid):
        self.cid = cid
        self.nodes = set()      # set of nodes in this component
        self.edges = set()      # edges to other components
        self.good = False

# Find strongly connected components using Kosaraju's algorithm
def find_scc(nodes):
    stack = []
    kosaraju1(nodes, stack)
    seen = set()
    components = []
    while stack != []:
        next = stack.pop()
        if next.uid not in seen:
            scc = SCC(len(components))
            components.append(scc)
            kosaraju2(nodes, next, seen, scc)
    return components

def run(code, labels, blockflag):
    state = State(code, labels)
    ctx = ContextValue(("__init__", None, None, None), 0, novalue, novalue)
    ctx.atomic = 1
    ctx.push("process")
    ctx.push(novalue)
    bag_add(state.ctxbag, ctx)
    node = Node(state, 0, None, None, None, [], 0)

    nodes = [node]

    # For traversing Kripke graph
    visited = { state: node }
    todo = collections.deque([node])
    bad = set()

    faultyState = False
    maxdiameter = 0
    while todo:
        node = todo.popleft()

        # check the invariants
        if len(node.issues) == 0 and node.state.choosing == None:
            for inv in node.state.invariants:
                if not invcheck(node.state, inv):
                    (lexeme, file, line, column) = code[inv].token
                    node.issues.add("Invariant file=%s line=%d failed"%(file, line))

        if len(node.issues) > 0:
            bad.add(node)
            faultyState = True
            break

        if node.expanded:
            continue
        node.expanded = True
        if node.len > maxdiameter:
            maxdiameter = node.len

        if node.state.choosing != None:
            ctx = node.state.choosing
            assert ctx in node.state.ctxbag, ctx
            choices = ctx.stack[-1]
            assert isinstance(choices, SetValue), choices
            assert len(choices.s) > 0
            for choice in choices.s:
                onestep(node, ctx, choice, False, nodes, visited, todo)
        else:
            for (ctx, _) in node.state.ctxbag.items():
                onestep(node, ctx, None, False, nodes, visited, todo)
                if ctx.trap != None and not ctx.interruptLevel:
                    onestep(node, ctx, None, True, nodes, visited, todo)

    if not silent:
        print("#states =", len(visited), "diameter =", maxdiameter,
                                " "*100 + "\b"*100)

    todump = set()

    # See if there has been a safety violation
    issues_found = False
    if len(bad) > 0:
        print("==== Safety violation ====")
        bad_node = find_shortest(bad)
        print_path(bad_node)
        todump.add(bad_node)
        for issue in bad_node.issues:
            print(issue)
        issues_found = True

    if not faultyState:
        # Determine the strongly connected components
        components = find_scc(nodes)
        if not silent:
            print("#components:", len(components))

        # Figure out which strongly connected components are "good".
        # These are non-sink components or components that have
        # a terminated state.
        bad = set()
        for (s, n) in visited.items():
            if len(s.ctxbag) == 0 and len(s.stopbag) == 0:
                assert len(n.edges) == 0
                components[n.cid].good = True
                if blockflag:
                    bad.add(n)
                    n.issues.add("Terminating State")
            else:
                # assert len(n.edges) != 0, n.edges         TODO
                for (nn, nc, steps) in n.edges.values():
                    if nn.cid != n.cid:
                        components[n.cid].edges.add(nn.cid)
                    if nn.cid != n.cid:
                        components[n.cid].good = True
                        break

        nbadc = sum(not scc.good for scc in components)
        if nbadc != 0:
            if not blockflag:
                print("#bad components:", nbadc)
            for n in nodes:
                if components[n.cid].good:
                    continue
                if blockflag:
                    # see if all processes are blocked or stopped
                    s = n.state
                    for ctx in s.ctxbag.keys():
                        assert isinstance(ctx, ContextValue)
                        if not n.isblocked(ctx):
                            n.issues.add("Non-terminating State")
                            bad.add(n)
                            break
                else:
                    n.issues.add("Non-terminating State")
                    bad.add(n)

        if len(bad) > 0:
            bad_node = find_shortest(bad)
            issues = ""
            for issue in bad_node.issues:
                if issues != "":
                    issues += ", "
                issues += issue
            print("====", issues, "===")
            print_path(bad_node)
            todump.add(bad_node)
            issues_found = True

            # See which processes are blocked
            assert not bad_node.state.choosing
            running = 0
            blocked = 0
            stopped = 0
            for ctx in bad_node.state.ctxbag.keys():
                assert isinstance(ctx, ContextValue)
                if bad_node.isblocked(ctx):
                    blocked += 1
                    print("blocked process:", ctx.nametag(), "pc =", ctx.pc)
                else:
                    running += 1
                    print("running process:", ctx.nametag(), "pc =", ctx.pc)
            for ctx in bad_node.state.stopbag.keys():
                print("stopped process:", ctx.nametag(), "pc =", ctx.pc)
                stopped += 1
            print("#blocked:", blocked, "#stopped:", stopped, "#running:", running)

    if not issues_found:
        print("no issues found")
        n = None
    else:
        n = find_shortest(todump)
    return (nodes, n)

def htmlstrsteps(steps):
    if steps == None:
        return "[]"
    result = ""
    i = 0
    while i < len(steps):
        if result != "":
            result += " "
        (pc, choice) = steps[i]
        j = i + 1
        if pc == None:
            result += "Interrupt"
        else:
            result += "<a href='#P%d'>%d"%(pc, pc)
        if choice != None:
            result += "</a>(choose %s)"%strValue(choice)
        else:
            while j < len(steps):
                (pc2, choice2) = steps[j]
                if pc == None or pc2 != pc + 1 or choice2 != None:
                    break
                (pc, choice) = (pc2, choice2)
                j += 1
            if j > i + 1:
                result += "-%d"%pc
            result += "</a>"
        i = j
    return result

def genpath(n):
    # Extract the path to node n
    path = []
    while n != None:
        if n.after == None:
            break
        path = [n] + path
        n = n.parent

    # Now compress the path, combining macrosteps by the same context
    path2 = []
    lastctx = firstctx = None
    laststeps = []
    laststates = []
    lastvars = DictValue({})
    for n in path:
        if firstctx == None:
            firstctx = n.before
        if lastctx == None or lastctx == n.before:
            laststeps += n.steps
            lastctx = n.after
            laststates.append(n.uid)
            lastvars = n.state.vars
            continue
        path2.append((firstctx, lastctx, laststeps, laststates, lastvars))
        firstctx = n.before
        lastctx = n.after
        laststeps = n.steps.copy()
        laststates = [n.uid]
        lastvars = n.state.vars
    path2.append((firstctx, lastctx, laststeps, laststates, lastvars))
    return path2

def vardim(d):
    totalwidth = 0
    maxheight = 0
    if isinstance(d, dict):
        for k in sorted(d.keys()):
            (w, h) = vardim(d[k])
            totalwidth += w
            if h + 1 > maxheight:
                maxheight = h + 1
    else:
        return (1, 0)
    return (totalwidth, maxheight)

def varhdr(d, name, nrows, f):
    q = queue.Queue()
    level = 0
    q.put((d, level))
    while not q.empty():
        (nd, nl) = q.get()
        if nl > level:
            print("</tr><tr>", file=f)
            level = nl
        if isinstance(nd, dict):
            for k in sorted(nd.keys()):
                (w,h) = vardim(nd[k])
                if h == 0:
                    print("<td align='center' style='font-style: italic' colspan=%d rowspan=%d>%s</td>"%(w,nrows-nl,k), file=f)
                else:
                    print("<td align='center' style='font-style: italic' colspan=%d>%s</td>"%(w,k), file=f)
                q.put((nd[k], nl+1))

def vardump_rec(d, vars, f):
    if isinstance(d, dict):
        for k in sorted(d.keys()):
            if vars != None and k in vars.d:
                vardump_rec(d[k], vars.d[k], f)
            else:
                vardump_rec(d[k], None, f)
    elif vars == None:
        print("<td></td>", file=f)
    else:
        print("<td align='center'>%s</td>"%strValue(vars), file=f)

def vardump(d, vars, f):
    for k in sorted(d.keys()):
        vardump_rec(d[k], vars.d[k], f)

def htmlpath(n, color, f):
    # Generate a label for the path table
    issues = n.issues
    if len(issues) == 0:
        issues = { "no issues" }
    label = ""
    for issue in issues:
        if label != "":
            label += ", "
        label += issue
    label = "Issue: " + label
    # keys = sorted(n.state.vars.d.keys(), key=keyValue)
    path = genpath(n)
    d = pathvars(path)
    (width, height) = vardim(d)
    print("<table id='issuestbl' border='1' width='100%%'><tr><th colspan='2' align='left' style='color: %s'>%s</th><th></th>"%(color, html.escape(label)), file=f)
    if width == 1:
        print("<th>Shared Variable</th>", file=f)
    else:
        print("<th colspan='%d'>Shared Variables</th>"%width, file=f)
    print("<col style='width:15%'>", file=f)
    print("<tr><th rowspan=%d>Process</th><th rowspan=%d>Steps</th><th rowspan=%d></th>"%(height, height, height), file=f)
    varhdr(d, "", height, f)
    print("</tr><tr><td></td></tr>", file=f)
    row = height + 1
    pids = []
    for (fctx, ctx, steps, states, vars) in path:
        row += 1
        if len(states) > 0:
            sid = states[-1]
        else:
            sid = n.uid
        try:
            pid = pids.index(fctx)
            pids[pid] = ctx
        except ValueError:
            pids.append(ctx)
            pid = len(pids) - 1
        print("<tr><td>T%d: <a href='javascript:rowshow(%d,%d)'>%s</a></td>"%(pid, row, sid, ctx.nametag()), file=f)
        print("<td>%s</td><td></td>"%htmlstrsteps(steps), file=f)
        vardump(d, vars, f)
        print("</tr>", file=f)
    print("</table>", file=f)
    return height

def htmlloc(code, scope, ctx, traceid, f):
    pc = ctx.pc
    fp = ctx.fp
    print("<table id='loc%d' border='1' width='100%%'>"%traceid, file=f)
    trace = []
    while True:
        trace += [(pc, fp)]
        if fp < 5:
            break
        pc = ctx.stack[fp - 5]
        assert isinstance(pc, PcValue)
        pc = pc.pc
        fp = ctx.stack[fp - 1]
    trace.reverse()
    row = 0
    for (pc, fp) in trace:
        if row == 0:
            print("<tr style='background-color: #A5FF33'>", file=f)
        else:
            print("<tr>", file=f)
        print("<td>", file=f)
        print("<a href='#P%d'>%d</a> "%(pc, pc), file=f)
        print("<a href='javascript:setrow(%d,%d)'>"%(traceid,row), file=f)
        origpc = pc
        while pc >= 0 and pc not in scope.locations:
            pc -= 1
        if pc in scope.locations:
            (file, line) = scope.locations[pc]
        else:
            (file, line) = ("NOFILE", 0)
        # TODO.  Should skip over nested methods
        while pc >= 0 and not isinstance(code[pc], FrameOp):
            pc -= 1
        if fp >= 3:
            arg = ctx.stack[fp-3]
            if arg == novalue:
                print("%s()"%(code[pc].name[0]), end="", file=f)
            else:
                print("%s(%s)"%(code[pc].name[0], strValue(arg)), end="", file=f)
        print("</a>:", file=f)
        lines = files.get(file)
        if lines != None and line <= len(lines):
            print(html.escape(lines[line - 1]), file=f)
        print("</td></tr>", file=f)
        row += 1

    if ctx.failure != None:
        print("<tr style='color: red'><td>%s</td></tr>"%ctx.failure, file=f)
    print("</table>", file=f)

def htmlvars(vars, id, row, f):
    assert(isinstance(vars, DictValue))
    display = "block" if row == 0 else "none"
    print("<div id='vars%d_%d' style='display:%s'>"%(traceid, row, display), file=f)
    if len(vars.d) > 0:
        print("<table>", file=f)
        for (key, value) in vars.d.items():
            print("<tr>", file=f)
            print("<td>%s = %s</td>"%(strValue(key)[1:], strValue(value)), file=f)
            print("</tr>", file=f)
        print("</table>", file=f)
    print("</div>", file=f)

# print the variables on the stack
def htmltrace(code, scope, ctx, traceid, f):
    pc = ctx.pc
    fp = ctx.fp
    trace = [ctx.vars]
    while True:
        if fp < 5:
            break
        trace.append(ctx.stack[fp - 2])
        fp = ctx.stack[fp - 1]
    trace.reverse()
    for i in range(len(trace)):
        htmlvars(trace[i], traceid, i, f)

traceid = 0

def htmlrow(ctx, bag, node, code, scope, f, verbose):
    global traceid
    traceid += 1

    print("<tr>", file=f)
    if bag[ctx] > 1:
        print("<td>%s [%d copies]</td>"%(ctx.nametag(), bag[ctx]), file=f)
    else:
        print("<td>%s</td>"%ctx.nametag(), file=f)
    if ctx.stopped:
        print("<td>stopped</td>", file=f)
    else:
        if node.state.choosing:
            print("<td>choosing</td>", file=f)
        else:
            if ctx in node.edges:
                if node.isblocked(ctx):
                    print("<td>blocked</td>", file=f)
                else:
                    print("<td>running</td>", file=f)
            else:
                print("<td>failed</td>", file=f)

    print("<td>", file=f)
    htmlloc(code, scope, ctx, traceid, f)
    print("</td>", file=f)

    # print variables
    print("<td>", file=f)
    htmltrace(code, scope, ctx, traceid, f)
    print("</td>", file=f)

    # print stack
    if verbose:
        print("<td>%d</td>"%ctx.fp, file=f)
        print("<td align='center'>", file=f)
        print("<table border='1'>", file=f)
        for v in ctx.stack:
            print("<tr><td align='center'>", file=f)
            if isinstance(v, PcValue):
                print("<a href='#P%d'>"%v.pc, file=f)
                print("%s"%strValue(v), file=f)
                print("</a>", file=f)
            else:
                print("%s"%strValue(v), file=f)
            print("</td></tr>", file=f)
        print("</table>", file=f)
        print("</td>", file=f)
        assert not s.choosing
        if ctx in n.edges:
            (nn, nc, steps) = n.edges[ctx]
            print("<td>%s</td>"%htmlstrsteps(steps), file=f)
            print("<td><a href='javascript:show(%d)'>"%nn.uid, file=f)
            print("%d</a></td>"%nn.uid, file=f)
        else:
            print("<td>no steps</td>", file=f)
            print("<td></td>", file=f)
    print("</tr>", file=f)

def htmlstate(f):
    print("<table border='1' width='90%'>", file=f)
    print("<col style='width:20%'>", file=f)
    print("<col style='width:80%'>", file=f)

    print("<tr><td>state id</td><td>%d</td></tr>"%n.uid, file=f)
    # if s.failure != None:
    #     print("<tr><td>status</td><td>failure</td></tr>", file=f)
    if s.initializing:
        print("<tr><td>status</td><td>initializing</td></tr>", file=f)
    elif len(s.ctxbag) == 0:
        if len(s.stopbag) == 0:
            print("<tr><td>status</td><td>terminal</td></tr>", file=f)
        else:
            print("<tr><td>status</td><td>stopped</td></tr>", file=f)
    else:
        print("<tr><td>status</td><td>normal</td></tr>", file=f)

    if verbose:
        print("<tr><td>from</td>", file=f)
        print("<td><table><tr>", file=f)
        for src in sorted(n.sources, key=lambda x: (x.len, x.uid)):
            print("<td><a href='javascript:show(%d)'>%d</td>"%(src.uid, src.uid), file=f)
        print("</tr></table></td></tr>", file=f)

    if s.choosing != None:
        print("<tr><td>choosing</td><td>%s</td></tr>"%s.choosing.nametag(), file=f)

    print("</table>", file=f)

def htmlnode(n, code, scope, f, verbose):
    print("<div id='div%d' style='display:none'>"%n.uid, file=f)
    print("<div class='container'>", file=f)

    print("<a name='N%d'/>"%n.uid, file=f)

    if verbose:
        print("<td>", file=f)
        height = htmlpath(n, "black", f)
        print("</td>", file=f)

    # if n.state.failure != None:
    #     print("<table border='1' style='color: red'><tr><td>Failure:</td>", file=f)
    #     print("<td>%s</td>"%n.state.failure, file=f)
    #     print("</tr></table>", file=f)

    print("<table border='1'>", file=f)
    print("<tr><th>Process</th><th>Status</th><th>Stack Trace</th><th>Variables</th>", file=f)
    if verbose:
        print("<th>FP</th><th>Stack</th>", file=f)
        print("<th>Steps</th><th>Next State</th></tr>", file=f)
    else:
        print("</tr>", file=f)
        print("<tr><td></td><td></td><td></td><td></td></tr>", file=f)
    for ctx in sorted(n.state.ctxbag.keys(), key=lambda x: x.nametag()):
        htmlrow(ctx, n.state.ctxbag, n, code, scope, f, verbose)
    for ctx in sorted(n.state.stopbag.keys(), key=lambda x: x.nametag()):
        htmlrow(ctx, n.state.stopbag, n, code, scope, f, verbose)

    print("</table>", file=f)
    print("</div>", file=f)
    print("</div>", file=f)

def htmlcode(code, scope, f):
    assert False
    print("<div id='table-wrapper'>", file=f)
    print("<div id='table-scroll'>", file=f)
    print("<table border='1'>", file=f)
    print("<tbody>", file=f)
    lastloc = None
    for pc in range(len(code)):
        print("<tr>", file=f)
        if scope.locations.get(pc) != None:
            (file, line) = scope.locations[pc]
            if (file, line) != lastloc:
                lines = files.get(file)
                if lines != None and line <= len(lines):
                    print("<th colspan='3' align='left' style='background-color: yellow'>%s:%d"%(html.escape(os.path.basename(file)), line),
                        html.escape(lines[line - 1]), "</th>", file=f)
                else:
                    print("<th colspan='2' align='left'>Line", line, "</th>", file=f)
                print("</tr><tr>", file=f)
            lastloc = (file, line)
        print("<td><a name='P%d'>"%pc, pc, "</a></td><td>", file=f)
        print("<span title='%s'>"%html.escape(code[pc].explain()), file=f)
        if isinstance(code[pc], JumpOp) or isinstance(code[pc], JumpCondOp):
            print("<a href='#P%d'>"%code[pc].pc, code[pc], "</a>", file=f)
        elif isinstance(code[pc], PushOp) and isinstance(code[pc].constant[0], PcValue):
            print("Push <a href='#P%d'>"%code[pc].constant[0].pc, strValue(code[pc].constant[0]), "</a>", file=f)
        else:
            print(html.escape(str(code[pc])), file=f)
        print("</span></td></tr>", file=f)
    print("</tbody>", file=f)
    print("</table>", file=f)
    print("</div>", file=f)
    print("</div>", file=f)

def htmldump(nodes, code, scope, node, fulldump, verbose):
    with open("harmony.html", "w", encoding='utf-8') as f:
        print("""
<html>
  <head>
    <style>
#table-wrapper {
  position:relative;
}
#table-scroll {
  height:200px;
  overflow:auto;  
}
#table-wrapper table {
  width:100%;
}
#table-wrapper table * {
  color:black;
}
#table-wrapper table thead th .text {
  position:absolute;   
  top:-20px;
  z-index:2;
  height:20px;
  width:35%;
  border:1px solid red;
}
table {
    border-collapse: collapse;
    border-style: hidden;
}
table td, table th {
    border: 1px solid black;
}
    </style>
  </head>
  <body>
        """, file=f)

        print("<table>", file=f)
        print("<col style='width:50%'>", file=f)
        print("<col style='width:50%'>", file=f)

        if node != None:
            print("<tr><td colspan='2'>", file=f)
            height = htmlpath(node, "red", f)
            print("</td></tr>", file=f)
            print("<tr><td></td></tr>", file=f)

        print("<tr>", file=f)

        print("<td valign='top'>", file=f)
        htmlcode(code, scope, f)
        print("</td>", file=f)

        print("<td valign='top'>", file=f)
        if fulldump:
            for n in nodes:
                htmlnode(n, code, scope, f, verbose)
        else:
            if node == None:
                cnt = 0
                for n in nodes:
                    htmlnode(n, code, scope, f, verbose)
                    cnt += 1
                    if not fulldump and cnt > 100:
                        break
            else:
                n = node
                while n != None:
                    htmlnode(n, code, scope, f, verbose)
                    n = n.parent
        print("</td>", file=f)
        print("</tr>", file=f)
        print("</table>", file=f)

        if node == None:
            row = 0
            sid = 1
        else:
            row = node.len + height + 1
            sid = node.uid
        print(
            """
                <div id='divNone' style='display:none';>
                  <div class='container'>
                    <p>
                        State information not available.
                        Use harmony -d for a complete htmldump.
                    </p>
                  </div>
                </div>

                <script>
                  var current = 1;

                  function show(id) {
                      x = document.getElementById('div' + current);
                      if (x == null) {
                          x = document.getElementById('divNone')
                      }
                      x.style.display = 'none';
                      x = document.getElementById('div' + id)
                      if (x == null) {
                          x = document.getElementById('divNone')
                      }
                      x.style.display = 'block';
                      current = id;
                  }

                  function rowshow(row, id) {
                    show(id);
                    var tbl = document.getElementById("issuestbl");
                    for (var i = 1; i < tbl.rows.length; i++) {
                        if (i == row + 1) {
                            tbl.rows[i].style.backgroundColor = "#A5FF33";
                        }
                        else {
                            tbl.rows[i].style.backgroundColor = "";
                        }
                    }
                  }

                  function setrow(tblid, row) {
                    var tbl = document.getElementById('loc' + tblid);
                    for (var i = 0; i < tbl.rows.length; i++) {
                        var div = document.getElementById('vars' + tblid + '_' + i);
                        if (i == row) {
                            tbl.rows[i].style.backgroundColor = "#A5FF33";
                            div.style.display = 'block';
                        }
                        else {
                            tbl.rows[i].style.backgroundColor = "";
                            div.style.display = 'none';
                        }
                    }
                  }

                  rowshow(%d, %d)
                </script>
            """%(row, sid), file=f)
        print("</body>", file=f)
        print("</html>", file=f)
    print("open file://" + os.getcwd() + "/harmony.html for more information")

def dumpCode(printCode, code, scope, f=sys.stdout):
    lastloc = None
    if printCode == "json":
        print("{", file=f)
        print('  "labels": {', file=f)
        for (k, v) in scope.labels.items():
            print('    "%s": "%d",'%(k, v), file=f)
        print('    "__end__": "%d"'%len(code.labeled_ops), file=f)
        print('  },', file=f)
        print('  "code": [', file=f)
    for pc in range(len(code.labeled_ops)):
        if printCode == "verbose":
            lop = code.labeled_ops[pc]
            file, line = lop.file, lop.line
            if file != None and (file, line) != lastloc:
                lines = files.get(file)
                if lines != None and line <= len(lines):
                    print("%s:%d"%(file, line), lines[line - 1], file=f)
                else:
                    print(file, ":", line, file=f)
                lastloc = (file, line)
            # for label in code.labeled_ops[pc].labels:
            #     if label.module == None:
            #         print("%s:"%label.label)
            #     else:
            #         print("%s.%s"%(label.module, label.label))
            print("  ", pc, code.labeled_ops[pc].op, file=f)
        elif printCode == "json":
            if pc < len(code.labeled_ops) - 1:
                print("    %s,"%code.labeled_ops[pc].op.jdump(), file=f)
            else:
                print("    %s"%code.labeled_ops[pc].op.jdump(), file=f)
        else:
            print(code.labeled_ops[pc].op, file=f)
    if printCode == "json":
        print("  ],", file=f)
        print('  "pretty": [', file=f)
        for pc in range(len(code.labeled_ops)):
            if pc < len(code.labeled_ops) - 1:
                print('    [%s,%s],'%(json.dumps(str(code.labeled_ops[pc].op), ensure_ascii=False), json.dumps(code.labeled_ops[pc].op.explain(), ensure_ascii=False)), file=f)
            else:
                print('    [%s,%s]'%(json.dumps(str(code.labeled_ops[pc].op), ensure_ascii=False), json.dumps(code.labeled_ops[pc].op.explain(), ensure_ascii=False)), file=f)
        print("  ],", file=f)
        print("  \"locations\": {", file=f, end="")
        firstTime = True
        for pc in range(len(code.labeled_ops)):
            lop = code.labeled_ops[pc]
            file, line = lop.file, lop.line
            if file != None:
                if firstTime:
                    firstTime = False
                    print(file=f)
                else:
                    print(",", file=f)
                print("    \"%d\": { \"file\": %s, \"line\": \"%d\", \"code\": %s }"%(pc, json.dumps(file, ensure_ascii=False), line, json.dumps(files[file][line-1], ensure_ascii=False)), file=f, end="")
        print(file=f)
        print("  }", file=f)
        print("}", file=f)

tladefs = """-------- MODULE Harmony --------
EXTENDS Integers, FiniteSets, Bags, Sequences, TLC

\* This is the Harmony TLA+ module.  All the Harmony virtual machine
\* instructions are defined below.  Mostly, if the Harmony VM instruction
\* is called X, then its definition below is under the name OpX.  There
\* are some cases where there is an extension.  For example, the Store
\* instruction has two versions: OpStore and OpStoreInd, depending on
\* whether the variable is directly specified or its address is on the
\* stack of the current thread.

\* There are three variables:
\*  active: a set of the currently active contexts
\*  ctxbag: a multiset of all contexts
\*  shared: a map of variable names to Harmony values
\*
\* A context is the state of a thread.  A context may be atomic or not.
\* There can be at most one atomic context.  If there is an atomic context,
\* it and only it is in the active set.  If there is no atomic context,
\* then the active set is the domain of the ctxbag.
VARIABLE active, ctxbag, shared
allvars == << active, ctxbag, shared >>

\* The variable "shared" is a Harmony dict type
SharedInvariant == shared.ctype = "dict"

TypeInvariant == SharedInvariant

\* Harmony values are represented by a ctype tag that contains the name of
\* their Harmony type and a cval that contains their TLA+ representation
HBool(x)    == [ ctype |-> "bool",    cval |-> x ]
HInt(x)     == [ ctype |-> "int",     cval |-> x ]
HStr(x)     == [ ctype |-> "str",     cval |-> x ]
HPc(x)      == [ ctype |-> "pc",      cval |-> x ]
HDict(x)    == [ ctype |-> "dict",    cval |-> x ]
HSet(x)     == [ ctype |-> "set",     cval |-> x ]
HAddress(x) == [ ctype |-> "address", cval |-> x ]
HContext(x) == [ ctype |-> "context", cval |-> x ]

\* Defining the Harmony constant (), which is an empty dict
EmptyFunc == [x \in {} |-> TRUE]
EmptyDict == HDict(EmptyFunc)

\* Defining the Harmony constant None, which is a empty address
None      == HAddress(<<>>)

\* Convenient definition for the "result" variable in each method
Result    == HStr("result")

\* Flatten a sequence of sequences
Flatten(seq) ==
    LET F[i \\in 0..Len(seq)] == IF i = 0 THEN <<>> ELSE F[i-1] \\o seq[i]
    IN F[Len(seq)]

\* Harmony values are ordered first by their type
HRank(x) ==
    CASE x.ctype = "bool"    -> 0
    []   x.ctype = "int"     -> 1
    []   x.ctype = "str"     -> 2
    []   x.ctype = "pc"      -> 3
    []   x.ctype = "dict"    -> 4
    []   x.ctype = "set"     -> 5
    []   x.ctype = "address" -> 6
    []   x.ctype = "context" -> 7

\* TLA+ does not seem to have a direct way to compare characters in a
\* string, so...  Note that this only contains the printable ASCII
\* characters and excludes the backquote and double quote characters
\* as well as the backslash
CRank(c) ==
    CASE c=" "->32[]c="!"->33[]c="#"->35[]c="$"->36[]c="%"->37[]c="&"->38
    []c="'"->39[]c="("->40[]c=")"->41[]c="*"->42[]c="+"->43[]c=","->44
    []c="-"->45[]c="."->46[]c="/"->47[]c="0"->48[]c="1"->49[]c="2"->50
    []c="3"->51[]c="4"->52[]c="5"->53[]c="6"->54[]c="7"->55[]c="8"->56
    []c="9"->57[]c=":"->58[]c=";"->59[]c="<"->60[]c="="->61[]c=">"->62
    []c="?"->63[]c="@"->64[]c="A"->65[]c="B"->66[]c="C"->67[]c="D"->68
    []c="E"->69[]c="F"->70[]c="G"->71[]c="H"->72[]c="I"->73[]c="J"->74
    []c="K"->75[]c="L"->76[]c="M"->77[]c="N"->78[]c="O"->79[]c="P"->80
    []c="Q"->81[]c="R"->82[]c="S"->83[]c="T"->84[]c="U"->85[]c="V"->86
    []c="W"->87[]c="X"->88[]c="Y"->89[]c="Z"->90[]c="["->91[]c="]"->93
    []c="^"->94[]c="_"->95[]c="a"->97[]c="b"->98[]c="c"->99
    []c="d"->100[]c="e"->101[]c="f"->102[]c="g"->103[]c="h"->104
    []c="i"->105[]c="j"->106[]c="k"->107[]c="l"->108[]c="m"->109
    []c="n"->110[]c="o"->111[]c="p"->112[]c="q"->113[]c="r"->114
    []c="s"->115[]c="t"->116[]c="u"->117[]c="v"->118[]c="w"->119
    []c="x"->120[]c="y"->121[]c="z"->122[]c="{"->123[]c="|"->124
    []c="}"->125[]c="~"->126

\* Comparing two TLA+ strings
RECURSIVE StrCmp(_,_)
StrCmp(x, y) ==
    IF x = y
    THEN
        0
    ELSE
        CASE Len(x) = 0 ->  1
        []   Len(y) = 0 -> -1
        [] OTHER ->
            LET rx == CRank(Head(x))
                ry == CRank(Head(y))
            IN
                CASE rx < ry -> -1
                []   rx > ry ->  1
                [] OTHER -> StrCmp(Tail(x), Tail(y))

\* Setting up to compare two arbitrary Harmony values
RECURSIVE SeqCmp(_,_)
RECURSIVE HCmp(_,_)
RECURSIVE HSort(_)
RECURSIVE DictSeq(_)

\* Given a Harmony dictionary, return a sequence of its key, value
\* pairs sorted by the corresponding key.
DictSeq(dict) ==
    LET dom == HSort(DOMAIN dict)
    IN [ x \in 1..Len(dom) |-> << dom[x], dict[dom[x]] >> ]

\* Two dictionaries are ordered by their sequence of (key, value) pairs
\* Equivalently, we can flatten the sequence of (key, value) pairs first
\* into a single sequence of alternating keys and values.  Then we
\* compare the two sequences.
DictCmp(x, y) == SeqCmp(Flatten(DictSeq(x)), Flatten(DictSeq(y)))

\* Lexicographically compare two sequences of Harmony values
SeqCmp(x, y) ==
    IF x = y
    THEN
        0
    ELSE
        CASE Len(x) = 0 ->  1
        []   Len(y) = 0 -> -1
        [] OTHER ->
            LET c == HCmp(Head(x), Head(y))
            IN
                CASE c < 0 -> -1
                []   c > 0 ->  1
                [] OTHER -> SeqCmp(Tail(x), Tail(y))

\* Compare two contexts.  Essentially done lexicographically
CtxCmp(x, y) ==
    IF x = y THEN 0
    ELSE IF x.pc # y.pc THEN x.pc - y.pc
    ELSE IF x.apc # y.apc THEN x.apc - y.apc
    ELSE IF x.atomic # y.atomic THEN x.atomic - y.atomic
    ELSE IF x.vs # y.vs THEN DictCmp(x.vs, y.vs)
    ELSE IF x.stack # y.stack THEN SeqCmp(x.stack.cval, y.stack.cal)
    ELSE IF x.interruptLevel # y.interruptLevel THEN
             IF x.interruptLevel THEN -1 ELSE 1
    ELSE IF x.trap # y.trap THEN SeqCmp(x.trap, y.trap)
    ELSE IF x.readonly # y.readonly THEN x.readonly - y.readonly
    ELSE Assert(FALSE, "CtxCmp: this should not happen")

\* Compare two Harmony values as specified in the book
\* Return negative if x < y, 0 if x = y, and positive if x > y
HCmp(x, y) ==
    IF x = y
    THEN
        0
    ELSE
        IF x.ctype = y.ctype
        THEN 
            CASE x.ctype = "bool"    -> IF x.cval THEN 1 ELSE -1
            []   x.ctype = "int"     -> x.cval - y.cval
            []   x.ctype = "str"     -> StrCmp(x.cval, y.cval)
            []   x.ctype = "pc"      -> x.cval - y.cval
            []   x.ctype = "set"     -> SeqCmp(HSort(x.cval), HSort(y.cval))
            []   x.ctype = "dict"    -> DictCmp(x.cval, y.cval)
            []   x.ctype = "address" -> SeqCmp(x.cval, y.cval)
            []   x.ctype = "context" -> CtxCmp(x.cval, y.cval)
        ELSE
            HRank(x) - HRank(y)

\* The minimum and maximum Harmony value in a set
HMin(s) == CHOOSE x \in s: \A y \in s: HCmp(x, y) <= 0
HMax(s) == CHOOSE x \in s: \A y \in s: HCmp(x, y) >= 0

\* Sort a set of Harmony values into a sequence
HSort(s) ==
    IF s = {}
    THEN
        <<>>
    ELSE
        LET min == HMin(s) IN << min >> \\o HSort(s \\ {min})

\* This is to represent "variable name hierarchies" used in expressions
\* such as (x, (y, z)) = (1, (2, 3))
VName(name) == [ vtype |-> "var", vname |-> name ]
VList(list) == [ vtype |-> "tup", vlist |-> list ]

\* Representation of a context (the state of a thread).  It includes
\* the following fields:
\*  pc:     the program counter (location in the code)
\*  apc:    if atomic, the location in the code where the thread became atomic
\*  atomic: a counter: 0 means not atomic, larger than 0 is atomic
\*  vs:     a Harmony dictionary containing the variables of this thread
\*  stack:  a sequence of Harmony values
\*  interruptLevel: false if enabled, true if disabled
\*  trap:   either <<>> or a tuple containing the trap method and argument
\*  readonly: larger than 0 means not allowed to modify shared state
Context(pc, atomic, vs, stack, interruptLevel, trap, readonly) ==
    [
        pc             |-> pc,
        apc            |-> pc,
        atomic         |-> atomic,
        vs             |-> vs,
        stack          |-> stack,
        interruptLevel |-> interruptLevel,
        trap           |-> trap,
        readonly       |-> readonly
    ]

\* An initial context of a thread.  arg is the argument given when the thread
\* thread was spawned.  "process" is used by the OpReturn operator.
InitContext(pc, atomic, arg) ==
    Context(pc, atomic, EmptyDict, << arg, "process" >>, FALSE, <<>>, 0)

\* Update the given map with a new key -> value mapping
UpdateMap(map, key, value) ==
    [ x \\in (DOMAIN map) \\union {key} |-> IF x = key THEN value ELSE map[x] ]

\* Update a Harmony dictionary with a new key -> value mapping
UpdateDict(dict, key, value) ==
    HDict(UpdateMap(dict.cval, key, value))

\* The initial state of the Harmony module consists of a single thread starting
\* at pc = 0 and an empty set of shared variables
Init ==
    LET ctx == InitContext(0, 1, EmptyDict)
    IN /\\ active = { ctx }
       /\\ ctxbag = SetToBag(active)
       /\\ shared = EmptyDict

\* The state of the current thread goes from 'self' to 'next'.  Update
\* both the context bag and the active set
UpdateContext(self, next) ==
    /\\ active' = (active \\ { self }) \\union { next }
    /\\ ctxbag' = (ctxbag (-) SetToBag({self})) (+) SetToBag({next})

\* Remove context from the active set and context bag.  Make all contexts
\* in the context bag active
RemoveContext(self) ==
    /\\ ctxbag' = ctxbag (-) SetToBag({self})
    /\\ active' = BagToSet(ctxbag')

\* A Harmony address is essentially a sequence of Harmony values
\* These compute the head (the first element) and the remaining tail
AddrHead(addr) == Head(addr.cval)
AddrTail(addr) == HAddress(Tail(addr.cval))

\* Given a non-negative integer, return a sequence of bits starting
\* with least significant one
RECURSIVE Int2BitsHelp(_)
Int2BitsHelp(x) ==
    IF x = 0
    THEN <<>>
    ELSE <<x % 2 = 1>> \o Int2BitsHelp(x \\div 2)

\* Convert an integer to a bit sequence, lsb first. neg indicates if the
\* value is negative.
Int2Bits(x) ==
    IF x < 0
    THEN [ neg |-> TRUE,  bits |-> Int2BitsHelp(-x-1) ]
    ELSE [ neg |-> FALSE, bits |-> Int2BitsHelp(x)    ]

\* Convert a bit sequence (lsb first) to a non-negative integer
RECURSIVE Bits2IntHelp(_)
Bits2IntHelp(x) == 
    IF x = <<>>
    THEN 0
    ELSE (IF Head(x) THEN 1 ELSE 0) + 2 * Bits2IntHelp(Tail(x))

\* Convert a bit sequence to an integer.
Bits2Int(b) ==
    IF b.neg
    THEN -Bits2IntHelp(b.bits) - 1
    ELSE Bits2IntHelp(b.bits)

\* Compute the bitwise negation of a bit sequence
BitsNegate(b) == [ neg |-> ~b.neg, bits |-> b.bits ]

\* Compute b >> n
BitsShiftRight(b, n) ==
    IF n >= Len(b.bits)
    THEN [ neg |-> b.neg, bits |-> <<>> ]
    ELSE [ neg |-> b.neg, bits |-> SubSeq(b.bits, n + 1, Len(b.bits)) ]

\* Compute b << n
BitsShiftLeft(b, n) ==
    [ neg |-> b.neg, bits |-> [ x \in 1..n |-> b.neg ] \o b.bits ]

\* Helper functions for BitsXOR
RECURSIVE BitsXORhelp(_,_)
BitsXORhelp(x, y) ==
    CASE x = <<>> -> y
    []   y = <<>> -> x
    [] OTHER -> << Head(x) # Head (y) >> \o BitsXORhelp(Tail(x), Tail(y))

\* Compute x XOR y
BitsXOR(x, y) ==
    [ neg |-> x.neg # y.neg, bits |-> BitsXORhelp(x.bits, y.bits) ]

\* Helper function for BitsOr
RECURSIVE BitsOrHelp(_,_)
BitsOrHelp(x, y) ==
    CASE x.bits = <<>> -> IF x.neg THEN <<>> ELSE y.bits
    []   y.bits = <<>> -> IF y.neg THEN <<>> ELSE x.bits
    [] OTHER -> << (x.neg \\/ y.neg) #
            ((Head(x.bits) # x.neg) \\/ (Head(y.bits) # y.neg)) >> \o
            BitsOrHelp(
                [ neg |-> x.neg, bits |-> Tail(x.bits) ],
                [ neg |-> y.neg, bits |-> Tail(y.bits) ])

\* Compute x OR y
BitsOr(x, y) ==
    [ neg  |-> x.neg \\/ y.neg, bits |-> BitsOrHelp(x, y) ]

\* Helper function for BitsAnd
RECURSIVE BitsAndHelp(_,_)
BitsAndHelp(x, y) ==
    CASE x.bits = <<>> -> IF x.neg THEN y.bits ELSE <<>>
    []   y.bits = <<>> -> IF y.neg THEN x.bits ELSE <<>>
    [] OTHER -> << (x.neg /\\ y.neg) #
            ((Head(x.bits) # x.neg) /\\ (Head(y.bits) # y.neg)) >> \o
            BitsAndHelp(
                [ neg |-> x.neg, bits |-> Tail(x.bits) ],
                [ neg |-> y.neg, bits |-> Tail(y.bits) ])

\* Compute x AND y
BitsAnd(x, y) ==
    [ neg  |-> x.neg /\\ y.neg, bits |-> BitsAndHelp(x, y) ]

\* This is to implement del !addr, where addr is a Harmony address
\* (a sequence of Harmony values representing a path in dict, a tree of
\* dictionaries).  It is a recursive operator that returns the new dictionary.
RECURSIVE RemoveDictAddr(_, _)
RemoveDictAddr(dict, addr) ==
    HDict(
        IF Len(addr.cval) = 1
        THEN
            [ x \\in (DOMAIN dict.cval) \\ {AddrHead(addr)} |-> dict.cval[x] ]
        ELSE
            [ x \\in (DOMAIN dict.cval) |->
                IF x = AddrHead(addr)
                THEN
                      RemoveDictAddr(dict.cval[x], AddrTail(addr))
                ELSE
                    dict.cval[x]
            ]
    )

\* This is to implement !addr = value, where addr is a Harmony address
\* (a sequence of Harmony values representing a path in dict, a tree of
\* dictionaries), and value is the new value.  It is a recursive operator
\* that returns the new dictionary.
RECURSIVE UpdateDictAddr(_, _, _)
UpdateDictAddr(dict, addr, value) ==
    IF addr.cval = <<>>
    THEN
        value
    ELSE
        HDict(
            [ x \\in (DOMAIN dict.cval) \\union {AddrHead(addr)} |->
                IF x = AddrHead(addr)
                THEN
                      UpdateDictAddr(dict.cval[x], AddrTail(addr), value)
                ELSE
                    dict.cval[x]
            ]
        )

\* This is to compute the value of !addr in dict, which is a simple
\* recursive function
RECURSIVE LoadDictAddr(_, _)
LoadDictAddr(dict, addr) ==
    IF addr.cval = <<>>
    THEN
        dict
    ELSE
        LoadDictAddr(dict.cval[AddrHead(addr)], AddrTail(addr))

\* This is a helper operator for UpdateVars.
\* Harmony allows statements of the form: x,(y,z) = v.  For example,
\* if v = (1, (2, 3)), then this assigns 1 to x, 2 to y, and 3 to z.
\* For this operator, args is a tree describing the lefthand side,
\* while value is the righthand side of the equation above.  The
\* operator creates a sequence of (variable, value) records.  In the
\* example, the sequence would be << (x,1), (y,2), (z,3) >> essentially.
RECURSIVE CollectVars(_, _)
CollectVars(args, value) ==
    IF args.vtype = "var"
    THEN << [ var |-> HStr(args.vname), val |-> value ] >>
    ELSE
        Flatten([ i \\in DOMAIN args.vlist |->
            CollectVars(args.vlist[i], value.cval[HInt(i-1)])
        ])

\* Another helper operator for UpdateVars.  dict is a Harmony dictionary,
\* cv is a sequence as returned by CollectVars, and index is an index into
\* this sequence.  Fold returns an updated dictionary.
RECURSIVE Fold(_, _, _)
Fold(dict, cv, index) ==
    IF index = 0
    THEN dict
    ELSE
        LET elt == cv[index]
        IN Fold(UpdateDict(dict, elt.var, elt.val), cv, index - 1)

\* As explained in CollectVars, args is a tree of variable names that
\* appears on the lefthandside of a Harmony assignment operation.  value
\* is the value of the righthandside.  The vs are the variables of the
\* context that need to be updated.
UpdateVars(vs, args, value) ==
    LET cv == CollectVars(args, value)
    IN Fold(vs, cv, Len(cv))

\* A no-op
OpContinue(self) ==
    /\\ UpdateContext(self, [self EXCEPT !.pc = @ + 1])
    /\\ UNCHANGED shared

\* Pop the new interrupt level and push the old one
OpSetIntLevel(self) ==
    LET nl   == Head(self.stack)
        next == [self EXCEPT !.pc = @ + 1, !.interruptLevel = nl.cval,
            !.stack = << HBool(self.interruptLevel) >> \\o Tail(@)]
    IN
        /\\ nl.ctype = "bool"
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Increment the readonly counter (counter because of nesting)
OpReadonlyInc(self) ==
    LET next == [self EXCEPT !.pc = @ + 1, !.readonly = @ + 1]
    IN
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Decrement the readonly counter
OpReadonlyDec(self) ==
    LET next == [self EXCEPT !.pc = @ + 1, !.readonly = @ - 1]
    IN
        /\\ self.readonly > 0
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* This is used temporarily for Harmony VM instructions that have not yet
\* been implemented
Skip(self, what) == OpContinue(self)

\* First instruction of every method.  Saves the current variables on the stack,
\* Assigns the top of the stack to args (see UpdateVars) and initializes variable
\* result to None.
OpFrame(self, name, args) ==
    LET next == [
        self EXCEPT !.pc = @ + 1,
        !.stack = << self.vs >> \\o Tail(@),
        !.vs = UpdateVars(UpdateDict(@, Result, None), args, Head(self.stack))
    ]
    IN
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Remove one element from the stack
OpPop(self) ==
    LET next == [self EXCEPT !.pc = @ + 1, !.stack = Tail(@)]
    IN
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Remove key from the given map
DictCut(dict, key) == [ x \in (DOMAIN dict) \ { key } |-> dict[x] ]

\* s contains the name of a local variable containing a set, a dict, or a string
\* v contains the name of another local variable.  v can be a "variable tree"
\* (see UpdateVars).  The objective is to take the "smallest" element of s,
\* remove it from s, and assign it to v
OpCut(self, s, v) ==
    LET svar == HStr(s)
        sval == self.vs.cval[svar]
    IN
        CASE sval.ctype = "set" ->
            LET pick == HMin(sval.cval)
                intm == UpdateVars(self.vs, v, pick)
                next == [self EXCEPT !.pc = @ + 1,
                    !.vs = UpdateDict(intm, svar, HSet(sval.cval \\ {pick}))]
            IN
                /\\ UpdateContext(self, next)
                /\\ UNCHANGED shared
        [] sval.ctype = "dict" ->
            LET pick == HMin(DOMAIN sval.cval)
                intm == UpdateVars(self.vs, v, sval.cval[pick])
                next == [self EXCEPT !.pc = @ + 1,
                    !.vs = UpdateDict(intm, svar, HDict(DictCut(sval.cval, pick)))]
            IN
                /\\ UpdateContext(self, next)
                /\\ UNCHANGED shared
        [] sval.ctype = "str" ->
            LET intm == UpdateVars(self.vs, v, HStr(Head(sval.cval)))
                next == [self EXCEPT !.pc = @ + 1,
                    !.vs = UpdateDict(intm, svar, HStr(Tail(sval.cval)))]
            IN
                /\\ UpdateContext(self, next)
                /\\ UNCHANGED shared

\* d contains the name of a local variable containing a dict
\* v contains the name of another local variable.  v can be a "variable tree"
\* k contains the name of another local variable.  v can be a "variable tree"
\* (see UpdateVars).  The objective is to take the "smallest" element of d,
\* remove it from d, and assign it to k:v
OpCut3(self, d, v, k) ==
    LET dvar == HStr(d)
        dval == self.vs.cval[dvar]
    IN
        LET pick == HMin(DOMAIN dval.cval)
            intm == UpdateVars(UpdateVars(self.vs, v, dval.cval[pick]), k, pick)
            next == [self EXCEPT !.pc = @ + 1,
                !.vs = UpdateDict(intm, dvar, HDict(DictCut(dval.cval, pick)))]
        IN
            /\\ dval.ctype = "dict"
            /\\ UpdateContext(self, next)
            /\\ UNCHANGED shared

\* Delete the shared variable pointed to be v.  v is a sequence of Harmony
\* values acting as an address (path in hierarchy of dicts)
OpDel(self, v) ==
    /\\ Assert(self.readonly = 0, "Del in readonly mode")
    /\\ UpdateContext(self, [self EXCEPT !.pc = @ + 1])
    /\\ shared' = RemoveDictAddr(shared, HAddress(v))

\* Delete the shared variable whose address is pushed on the stack
OpDelInd(self) ==
    LET addr == Head(self.stack)
        next == [self EXCEPT !.pc = @ + 1, !.stack = Tail(@)]
    IN
        /\\ UpdateContext(self, next)
        /\\ shared' = RemoveDictAddr(shared, addr)

\* Delete the given local variable
OpDelVar(self, v) ==
    LET next == [self EXCEPT !.pc = @ + 1,
        !.vs = HDict([ x \in (DOMAIN @.cval) \\ { HStr(v.vname) } |-> @.cval[x] ]) ]
    IN
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Delete the local variable whose address is pushed on the stack
OpDelVarInd(self) ==
    LET addr == Head(self.stack)
        next == [self EXCEPT !.pc = @ + 1, !.stack = Tail(@),
                                    !.vs = RemoveDictAddr(@, addr)]
    IN
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Increment the given local variable
OpIncVar(self, v) ==
    LET var  == HStr(v.vname)
        next == [self EXCEPT !.pc = @ + 1,
                    !.vs = UpdateDict(@, var, HInt(@.cval[var].cval + 1)) ]
    IN
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Assign the top of the stack to a local variable
OpStoreVar(self, v) ==
    LET next == [self EXCEPT !.pc = @ + 1, !.stack = Tail(@), !.vs = UpdateVars(@, v, Head(self.stack))]
    IN
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Push the value of the given variable onto the stack
OpLoadVar(self, v) ==
    LET next == [self EXCEPT !.pc = @ + 1, !.stack = << self.vs.cval[HStr(v.vname)] >> \\o @ ]
    IN
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Increment the atomic counter for this thread.  If it was 0, boot every other
\* context out of the set of active contexts.
OpAtomicInc(self) ==
    IF self.atomic = 0
    THEN
        LET next == [self EXCEPT !.pc = @ + 1, !.apc = self.pc, !.atomic = 1]
        IN
            /\\ active' = { next }
            /\\ ctxbag' = (ctxbag (-) SetToBag({self})) (+) SetToBag({next})
            /\\ UNCHANGED shared
    ELSE
        LET next == [self EXCEPT !.pc = @ + 1, !.atomic = @ + 1]
        IN
            /\\ UpdateContext(self, next)
            /\\ UNCHANGED shared

\* Decrement the atomic counter.  If it becomes 0, let all other contexts
\* back into the active set.
OpAtomicDec(self) ==
    IF self.atomic = 1
    THEN
        LET next == [self EXCEPT !.pc = @ + 1, !.apc = 0, !.atomic = 0]
        IN
            /\\ ctxbag' = (ctxbag (-) SetToBag({self})) (+) SetToBag({next})
            /\\ active' = DOMAIN ctxbag'
            /\\ UNCHANGED shared
    ELSE
        LET next == [self EXCEPT !.pc = @ + 1, !.atomic = @ - 1]
        IN
            /\\ UpdateContext(self, next)
            /\\ UNCHANGED shared

\* Pop the top of stack and check if it is True.  If not, stop and print the
\* message.
OpAssert(self, msg) ==
    LET cond == Head(self.stack)
        next == [self EXCEPT !.pc = @ + 1, !.stack = Tail(@)]
    IN
        /\\ cond.ctype = "bool"
        /\\ Assert(cond.cval, msg)
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* The top of the stack contains an expression to be printed along with the
\* message if the next element on the stack is FALSE.
OpAssert2(self, msg) ==
    LET data == self.stack[1]
        cond == self.stack[2]
        next == [self EXCEPT !.pc = @ + 1, !.stack = Tail(Tail(@))]
    IN
        /\\ cond.ctype = "bool"
        /\\ Assert(cond.cval, << msg, data >>)
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Print what is on top of the stack (and pop it)
OpPrint(self) ==
    LET msg == Head(self.stack)
        next == [self EXCEPT !.pc = @ + 1, !.stack = Tail(@)]
    IN
        /\\ PrintT(msg)
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Pop the top of the stack, which must be a set.  Then select one of the
\* elements and push it back onto the stack.
OpChoose(self) ==
    LET choices == Head(self.stack)
    IN
        \\E v \\in choices.cval:
            LET next == [self EXCEPT !.pc = @ + 1, !.stack = <<v>> \\o Tail(@)]
            IN
                /\\ choices.ctype = "set"
                /\\ UpdateContext(self, next)
                /\\ UNCHANGED shared

\* "sequential" pops the address of a variable and indicates to the model
\* checker that the variable is assumed to have sequential consistency.
\* This turns off race condition checking for the variable.  For here, it can
\* just be considered a no-op.
OpSequential(self) == OpPop(self)

\* "invariant" is essentially a no-op.  Just skip over the code for the
\* invariant.
OpInvariant(self, end) ==
    /\\ UpdateContext(self, [self EXCEPT !.pc = end + 1])
    /\\ UNCHANGED shared

\* This is the general form of unary operators that replace the top of the
\* stack with a function computed over that value
OpUna(self, op(_)) ==
    LET e    == Head(self.stack)
        next == [self EXCEPT !.pc = @ + 1, !.stack = << op(e) >> \\o Tail(@)]
    IN
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Similar to OpUna but replaces two values on the stack with a single one.
OpBin(self, op(_,_)) ==
    LET e1   == self.stack[1]
        e2   == self.stack[2]
        next == [self EXCEPT !.pc = @ + 1,
            !.stack = << op(e2, e1) >> \\o Tail(Tail(@))]
    IN
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Apply binary operation op to first and the top of the stack n times
RECURSIVE StackFold(_,_,_,_)
StackFold(first, stack, op(_,_), n) ==
    IF n = 0
    THEN
        <<first>> \o stack
    ELSE
        StackFold(op(first, Head(stack)), Tail(stack), op, n - 1)

\* Like OpBin, but perform for top n elements of the stack
OpNary(self, op(_,_), n) ==
    LET e1   == Head(self.stack)
        ns   == StackFold(e1, Tail(self.stack), op, n - 1)
        next == [self EXCEPT !.pc = @ + 1, !.stack = ns ]
    IN
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Turn a Harmony list/tuple into a (reversed) sequence
List2Seq(list) ==
    LET n == Cardinality(DOMAIN list)
    IN [ i \in 1..n |-> list[HInt(n - i)] ]

\* Pop a tuple of the stack and push each of its n components
OpSplit(self, n) ==
    LET ns   == List2Seq(Head(self.stack).cval) \o Tail(self.stack)
        next == [self EXCEPT !.pc = @ + 1, !.stack = ns ]
    IN
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Move the stack element at position offset to the top
OpMove(self, offset) ==
    LET part1 == SubSeq(self.stack, 1, offset - 1)
        part2 == SubSeq(self.stack, offset, offset)
        part3 == SubSeq(self.stack, offset + 1, Len(self.stack))
        next  == [self EXCEPT !.pc = @ + 1, !.stack = part2 \o part1 \o part3 ]
    IN
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Duplicate the top of the stack
OpDup(self) ==
    LET next == [self EXCEPT !.pc = @ + 1, !.stack = <<Head(@)>> \o @]
    IN
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* The official "pc" of a thread depends on whether it is operating in
\* atomic mode or not.  If not, the pc is simply the current location
\* in the code.  However, if in atomic mode, the pc is the location where
\* the thread became atomic.
Location(ctx) == IF ctx.atomic > 0 THEN ctx.apc ELSE ctx.pc

\* Compute how many threads are currently at the given location
FunCountLabel(label) ==
    LET fdom == { c \\in DOMAIN ctxbag: Location(c) = label.cval }
        fbag == [ c \\in fdom |-> ctxbag[c] ]
    IN
        HInt(BagCardinality(fbag))

\* Convert the given integer into a string
RECURSIVE Int2Str(_)
Int2Str(x) ==
    IF x < 10
    THEN
        SubSeq("0123456789", x+1, x+1)
    ELSE
        LET rem == x % 10
        IN Int2Str(x \\div 10) \o SubSeq("0123456789", rem+1, rem+1)

\* Bunch of value to string conversion functions coming up
RECURSIVE Val2Str(_)
RECURSIVE Seq2Str(_)
RECURSIVE Addr2Str(_)
RECURSIVE Dict2StrHelp(_,_)

\* Convert a non-empty sequence of values to a string separated by commas
Seq2Str(x) ==
    IF Len(x) = 1
    THEN Val2Str(Head(x))
    ELSE Val2Str(Head(x)) \o ", " \o Seq2Str(Tail(x))

\* Convert a sequence of values of an address
Addr2Str(x) ==
    IF x = <<>>
    THEN ""
    ELSE "[" \o Val2Str(Head(x)) \o "]" \o Addr2Str(Tail(x))

\* Convert a non-empty dictionary to a string
Dict2StrHelp(keys, dict) ==
    LET first ==
        LET k == Head(keys) IN Val2Str(k) \o ": " \o Val2Str(dict[k])
    IN
        IF Len(keys) = 1
        THEN
            first
        ELSE
            first \o ", " \o Dict2StrHelp(Tail(keys), dict)

Dict2Str(x) == Dict2StrHelp(HSort(DOMAIN x), x)

\* Convert Harmony value x into a string
Val2Str(x) ==
    CASE x.ctype = "bool"    -> IF x.cval THEN "True" ELSE "False"
    []   x.ctype = "str"     -> "'" \o x.cval \o "'"
    []   x.ctype = "int"     -> Int2Str(x.cval)
    []   x.ctype = "pc"      -> "PC(" \o Int2Str(x.cval) \o ")"
    []   x.ctype = "dict"    ->
            IF DOMAIN x.cval = {} THEN "()" ELSE "{ " \o Dict2Str(x.cval) \o " }"
    []   x.ctype = "set"     ->
            IF x.cval = {} THEN "{}" ELSE "{ " \o Seq2Str(HSort(x.cval)) \o " }"
    []   x.ctype = "address" -> "?" \o Head(x.cval).cval \o Addr2Str(Tail(x.cval))

\* Compute the cardinality of a set of dict, or the length of a string
FunLen(s) ==
    CASE s.ctype = "set"  -> HInt(Cardinality(s.cval))
    []   s.ctype = "dict" -> HInt(Cardinality(DOMAIN s.cval))
    []   s.ctype = "str"  -> HInt(Len(s.cval))

\* Concatenate two sequences.  Helper function for FunAdd
DictConcat(x, y) ==
    LET xs  == Cardinality(DOMAIN x)
        ys  == Cardinality(DOMAIN y)
        dom == { HInt(i) : i \in 0 .. (xs + ys - 1) }
    IN
        [ i \in dom |-> IF i.cval < xs THEN x[i] ELSE y[HInt(i.cval - xs)] ]

\* Add two integers, or concatenate two sequences or strings
FunAdd(x, y) ==
    CASE x.ctype = "int"  /\\ y.ctype = "int"  -> HInt(x.cval + y.cval)
    []   x.ctype = "dict" /\\ y.ctype = "dict" -> HDict(DictConcat(x.cval, y.cval))
    []   x.ctype = "str"  /\\ y.ctype = "str"  -> HStr(x.cval \o y.cval)

\* Check to see if x is the empty set, dict, or string
FunIsEmpty(x) ==
    CASE x.ctype = "set"  -> HBool(x.cval = {})
    []   x.ctype = "dict" -> HBool((DOMAIN x.cval) = {})
    []   x.ctype = "str"  -> HBool(Len(x.cval) = 0)

\* Get the range of a dict (i.e., the values, not the keys)
Range(dict) == { dict[x] : x \in DOMAIN dict }

\* Get the minimum of a set or dict
FunMin(x) ==
    CASE x.ctype = "set"  -> HMin(x.cval)
    []   x.ctype = "dict" -> HMin(Range(x.cval))

\* Get the maximum of a set or dict
FunMax(x) ==
    CASE x.ctype = "set"  -> HMax(x.cval)
    []   x.ctype = "dict" -> HMax(Range(x.cval))

\* See if any element in the set or dict is true
FunAny(x) ==
    CASE x.ctype = "set"  -> HBool(HBool(TRUE) \in x.cval)
    []   x.ctype = "dict" -> HBool(HBool(TRUE) \in Range(x.cval))

\* See if all elements in the set of dict are true
FunAll(x) ==
    CASE x.ctype = "set"  -> HBool(x.cval = { HBool(TRUE) })
    []   x.ctype = "dict" -> HBool(HBool(FALSE) \\notin Range(x.cval))

\* Can be applied to integers or sets
FunSubtract(x, y) ==
    CASE x.ctype = "int" /\\ y.ctype = "int" -> HInt(x.cval - y.cval)
    []   x.ctype = "set" /\\ y.ctype = "set" -> HSet(x.cval \\ y.cval)

\* The following are self-explanatory
FunStr(v)           == HStr(Val2Str(v))
FunMinus(v)         == HInt(-v.cval)
FunNegate(v)        == HInt(Bits2Int(BitsNegate(Int2Bits(v.cval))))
FunAbs(v)           == HInt(IF v.cval < 0 THEN -v.cval ELSE v.cval)
FunNot(v)           == HBool(~v.cval)
FunKeys(x)          == HSet(DOMAIN x.cval)
FunRange(x, y)      == HSet({ HInt(i) : i \in x.cval .. y.cval })
FunEquals(x, y)     == HBool(x = y)
FunNotEquals(x, y)  == HBool(x /= y)
FunLT(x, y)         == HBool(HCmp(x, y) < 0)
FunLE(x, y)         == HBool(HCmp(x, y) <= 0)
FunGT(x, y)         == HBool(HCmp(x, y) > 0)
FunGE(x, y)         == HBool(HCmp(x, y) >= 0)
FunDiv(x, y)        == HInt(x.cval \\div y.cval)
FunMod(x, y)        == HInt(x.cval % y.cval)
FunPower(x, y)      == HInt(x.cval ^ y.cval)
FunSetAdd(x, y)     == HSet(x.cval \\union {y})
FunAddress(x, y)    == HAddress(x.cval \o <<y>>)
FunShiftRight(x, y) == HInt(Bits2Int(BitsShiftRight(Int2Bits(x.cval), y.cval)))
FunShiftLeft(x, y) == HInt(Bits2Int(BitsShiftLeft(Int2Bits(x.cval), y.cval)))

\* Compute either XOR of two ints or the union minus the intersection
\* of two sets
FunExclusion(x, y) ==
    CASE x.ctype = "set" /\\ y.ctype = "set" ->
        HSet((x.cval \\union y.cval) \\ (x.cval \\intersect y.cval))
    [] x.ctype = "int" /\\ y.ctype = "int" ->
        HInt(Bits2Int(BitsXOR(Int2Bits(x.cval), Int2Bits(y.cval))))

\* Merge two dictionaries.  If two keys conflict, use the minimum value
MergeDictMin(x, y) ==
    [ k \in DOMAIN x \\union DOMAIN y |->
        CASE k \\notin DOMAIN x -> y[k]
        []   k \\notin DOMAIN y -> x[k]
        [] OTHER -> IF HCmp(x[k], y[k]) < 0 THEN x[k] ELSE y[k]
    ]

\* Merge two dictionaries.  If two keys conflict, use the maximum value
MergeDictMax(x, y) ==
    [ k \in DOMAIN x \\union DOMAIN y |->
        CASE k \\notin DOMAIN x -> y[k]
        []   k \\notin DOMAIN y -> x[k]
        [] OTHER -> IF HCmp(x[k], y[k]) > 0 THEN x[k] ELSE y[k]
    ]

\* Union of two sets or dictionaries
\* TODO: also bitwise OR of integers
FunUnion(x, y) ==
    CASE x.ctype = "set" /\\ y.ctype = "set" ->
        HSet(x.cval \\union y.cval)
    [] x.ctype = "dict" /\\ y.ctype = "dict" ->
        HDict(MergeDictMax(x.cval, y.cval))
    [] x.ctype = "int" /\\ y.ctype = "int" ->
        HInt(Bits2Int(BitsOr(Int2Bits(x.cval), Int2Bits(y.cval))))

\* Intersection of two sets or dictionaries
FunIntersect(x, y) ==
    CASE x.ctype = "set" /\\ y.ctype = "set" ->
        HSet(x.cval \\intersect y.cval)
    [] x.ctype = "dict" /\\ y.ctype = "dict" ->
        HDict(MergeDictMin(x.cval, y.cval))
    [] x.ctype = "int" /\\ y.ctype = "int" ->
        HInt(Bits2Int(BitsAnd(Int2Bits(x.cval), Int2Bits(y.cval))))

\* See if x is in y, where y is a set, a dict, or a string. In case of
\* a string, check if x is a substring of y
FunIn(x, y) ==
    CASE y.ctype = "set"  -> HBool(x \in y.cval)
    []   y.ctype = "dict" -> HBool(\E k \in DOMAIN y.cval: y.cval[k] = x)
    []   y.ctype = "str"  ->
            LET xn == Len(x.cval)
                yn == Len(y.cval)
            IN
                HBool(\E i \in 0..(yn - xn): 
                    x.cval = SubSeq(y.cval, i+1, i+xn))

\* Concatenate n copies of dict, which represents a list
DictTimes(dict, n) ==
    LET odom == { x.cval : x \\in DOMAIN dict.cval }
        max  == CHOOSE x \in odom: \A y \in odom: y <= x
        card == max + 1
        ndom == { HInt(x): x \\in 0..(n.cval * card - 1) }
    IN
        HDict([ x \\in ndom |-> dict.cval[HInt(x.cval % card)] ])

\* Multiply two integers, or concatenate copies of a list
FunMult(e1, e2) ==
    CASE e1.ctype = "int" /\\ e2.ctype = "int" ->
        HInt(e2.cval * e1.cval)
    [] e1.ctype = "int" /\\ e2.ctype = "dict" ->
        DictTimes(e2, e1)
    [] e1.ctype = "dict" /\\ e2.ctype = "int" ->
        DictTimes(e1, e2)

\* By Harmony rules, if there are two conflicting key->value1 and key->value2
\* mappings, the higher values wins.
InsertMap(map, key, value) ==
    [ x \\in (DOMAIN map) \\union {key} |->
        IF x = key
        THEN
            IF x \\in DOMAIN map
            THEN
                IF HCmp(value, map[x]) > 0
                THEN
                    value
                ELSE
                    map[x]
            ELSE
                value
        ELSE
            map[x]
    ]

\* Push the current context onto the stack.  Pop the top "()" of the stack first.
OpGetContext(self) == 
    LET next  == [self EXCEPT !.pc = @ + 1,
                        !.stack = << HContext(self) >> \\o Tail(@)]
    IN
        /\\ Head(self.stack) = EmptyDict
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Pops a value, a key, and a dict, and pushes the dict updated to
\* reflect key->value.
OpDictAdd(self) ==
    LET value == self.stack[1]
        key   == self.stack[2]
        dict  == self.stack[3]
        newd  == HDict(InsertMap(dict.cval, key, value))
        next  == [self EXCEPT !.pc = @ + 1,
            !.stack = << newd >> \\o Tail(Tail(Tail(@)))]
    IN
        /\\ dict.ctype = "dict"
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Push Harmony constant c onto the stack.
OpPush(self, c) ==
    LET next == [self EXCEPT !.pc = @ + 1, !.stack = << c >> \\o @]
    IN
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* In Harmony, the expression "x(y)" (or equivalently "x y" or "x[y]")
\* means something different depending on the type of x, similar to TLA+
\* actually.  If x is a method, that x should be invoked with the argument y.
\* When the method finishes, the value is that of its "result" variable.
\* If x is a dictionary, then the value is that of x[y].  If x is a string,
\* then y must be an integer index and x[y] returns the specified character.
OpApply(self) ==
    LET arg    == self.stack[1]
        method == self.stack[2]
    IN
        CASE method.ctype = "pc" ->
            LET next == [self EXCEPT !.pc = method.cval,
                    !.stack = << arg, "normal", self.pc + 1 >> \\o Tail(Tail(@))]
            IN
                /\\ UpdateContext(self, next)
                /\\ UNCHANGED shared
        [] method.ctype = "dict" ->
            LET next == [self EXCEPT !.pc = @ + 1,
                            !.stack = << method.cval[arg] >> \\o Tail(Tail(@))]
            IN
                /\\ UpdateContext(self, next)
                /\\ UNCHANGED shared
        [] method.ctype = "str" ->
            LET char == SubSeq(method.cval, arg.cval+1, arg.cval+1)
                next == [self EXCEPT !.pc = @ + 1,
                    !.stack = << HStr(char) >> \\o Tail(Tail(@))]
            IN
                /\\ arg.ctype = "int"
                /\\ UpdateContext(self, next)
                /\\ UNCHANGED shared

\* Pop the top of the stack and store in the shared variable pointed to
\* by the sequence v of Harmony values that acts as an address
OpStore(self, v) ==
    LET next == [self EXCEPT !.pc = @ + 1, !.stack = Tail(@)]
    IN
        /\\ Assert(self.readonly = 0, "Store in readonly mode")
        /\\ UpdateContext(self, next)
        /\\ shared' = UpdateDictAddr(shared, HAddress(v), Head(self.stack))

\* Pop a value and an address and store the value at the given address
OpStoreInd(self) ==
    LET val  == self.stack[1]
        addr == self.stack[2]
        next == [self EXCEPT !.pc = @ + 1, !.stack = Tail(Tail(@))]
    IN
        /\\ Assert(self.readonly = 0, "StoreInd in readonly mode")
        /\\ UpdateContext(self, next)
        /\\ shared' = UpdateDictAddr(shared, addr, val)

\* Pop a value and an address and store the *local* value at the given address
OpStoreVarInd(self) ==
    LET val  == self.stack[1]
        addr == self.stack[2]
        next == [self EXCEPT !.pc = @ + 1, !.stack = Tail(Tail(@)),
                                    !.vs = UpdateDictAddr(@, addr, val)]
    IN
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Pop an address and push the value at the address onto the stack
OpLoadInd(self) ==
    LET
        addr == Head(self.stack)
        val  == LoadDictAddr(shared, addr)
        next == [self EXCEPT !.pc = @ + 1, !.stack = <<val>> \\o Tail(@)]
    IN
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Pop an address and push the value of the addressed local variable onto the stack
OpLoadVarInd(self) ==
    LET
        addr == Head(self.stack)
        val  == LoadDictAddr(self.vs, addr)
        next == [self EXCEPT !.pc = @ + 1, !.stack = <<val>> \\o Tail(@)]
    IN
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Push the value of shared variable pointed to by v onto the stack.  v
\* is a sequence of Harmony values acting as an address
OpLoad(self, v) ==
    LET next == [ self EXCEPT !.pc = @ + 1,
                    !.stack = << LoadDictAddr(shared, HAddress(v)) >> \\o @ ]
    IN
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Return the context and the given parameter
OpSave(self) ==
    LET valu == Head(self.stack)
        intm == [self EXCEPT !.pc = @ + 1, !.stack = Tail(@)]
        m1   == InsertMap(EmptyFunc, HInt(0), valu)
        m2   == InsertMap(m1, HInt(1), intm)
        next == [intm EXCEPT !.stack = << HDict(m2) >> \\o @]
    IN
        /\\ self.atomic > 0
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Store the context at the pushed address (unless it is None or ()) and
\* remove it from the  context bag and active set.  Make all contexts in
\* the context bag
OpStopInd(self) ==
    LET addr == Head(self.stack)
        next == [self EXCEPT !.pc = @ + 1, !.stack = Tail(@)]
    IN
        /\\ self.atomic > 0
        /\\ RemoveContext(self)
        /\\ IF addr = None \\/ addr = EmptyDict
            THEN
                UNCHANGED shared
            ELSE
                shared' = UpdateDictAddr(shared, addr, HContext(next))

\* What Return should do depends on whether the methods was spawned
\* or called as an ordinary method.  To indicate this, Spawn pushes the
\* string "process" on the stack, while Apply pushes the string "normal"
\* onto the stack.  The Frame operation also pushed the saved variables
\* which must be restored.
OpReturn(self) ==
    LET savedvars == self.stack[1]
        calltype  == self.stack[2]
    IN
        CASE calltype = "normal" ->
            LET raddr == self.stack[3]
                result == self.vs.cval[Result]
                next == [ self EXCEPT
                            !.pc = raddr,
                            !.vs = savedvars,
                            !.stack = << result >> \\o Tail(Tail(Tail(@)))
                        ]
            IN
                /\\ UpdateContext(self, next)
                /\\ UNCHANGED shared
        [] calltype = "interrupt" ->
            LET raddr == self.stack[3]
                next == [ self EXCEPT
                            !.pc = raddr,
                            !.interruptLevel = FALSE,
                            !.vs = savedvars,
                            !.stack = Tail(Tail(Tail(@)))
                        ]
            IN
                /\\ UpdateContext(self, next)
                /\\ UNCHANGED shared
        [] calltype = "process" ->
            /\\ ctxbag' = ctxbag (-) SetToBag({self})
            /\\ IF self.atomic > 0
               THEN active' = DOMAIN ctxbag'
               ELSE active' = active \\ { self }
            /\\ UNCHANGED shared

\* Set the program counter pc to the given value
OpJump(self, pc) ==
    LET next == [ self EXCEPT !.pc = pc ]
    IN
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Pop a value of the stack.  If it equals cond, set the pc to the
\* given value.
OpJumpCond(self, pc, cond) ==
    LET next == [ self EXCEPT !.pc = IF Head(self.stack) = cond
                    THEN pc ELSE (@ + 1), !.stack = Tail(@) ]
    IN
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Spawn a new thread.  If the current thread is not atomic, the
\* thread goes into the active set as well.
OpSpawn(self) ==
    LET local == self.stack[1]
        arg   == self.stack[2]
        entry == self.stack[3]
        next  == [self EXCEPT !.pc = @ + 1, !.stack = Tail(Tail(Tail(@)))]
        newc  == InitContext(entry.cval, 0, arg)
    IN
        /\\ entry.ctype = "pc"
        /\\ IF self.atomic > 0
           THEN active' = (active \\ { self }) \\union { next }
           ELSE active' = (active \\ { self }) \\union { next, newc }
        /\\ ctxbag' = (ctxbag (-) SetToBag({self})) (+) SetToBag({next,newc})
        /\\ UNCHANGED shared

\* Operation to set a trap.
OpTrap(self) ==
    LET entry == self.stack[1]
        arg   == self.stack[2]
        next  == [self EXCEPT !.pc = @ + 1, !.stack = Tail(Tail(@)),
                                        !.trap = << entry.cval, arg >>]
    IN
        /\\ entry.ctype = "pc"
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Restore a context that is pushed on the stack.  Also push the argument
\* onto the restored context's stack
\* TODO.  Currently arg and ctx are in the wrong order
OpGo(self) ==
    LET ctx  == self.stack[1]
        arg  == self.stack[2]
        next == [self EXCEPT !.pc = @ + 1, !.stack = Tail(Tail(@))]
        newc == [ctx.cval EXCEPT !.stack = << arg >> \o @]
    IN
        /\\ IF self.atomic > 0
            THEN active' = (active \\ { self }) \\union { next }
            ELSE active' = (active \\ { self }) \\union { next,newc }
        /\\ ctxbag' = (ctxbag (-) SetToBag({self})) (+) SetToBag({next,newc})
        /\\ UNCHANGED shared

\* When there are no threads left, the Idle action kicks in
Idle ==
    /\\ active = {}
    /\\ UNCHANGED allvars
"""

def tla_translate(f, code, scope):
    print(tladefs, file=f)
    first = True
    for pc in range(len(code.labeled_ops)):
        if first:
            print("Step(self) == ", end="", file=f)
            first = False
        else:
            print("              ", end="", file=f)
        print("\\/ self.pc = %d /\\ "%pc, end="", file=f)
        print(code.labeled_ops[pc].op.tladump(), file=f)
    print("""
Interrupt(self) ==
    LET next == [ self EXCEPT !.pc = self.trap[1],
                    !.stack = << self.trap[2], "interrupt", self.pc >> \o @,
                    !.interruptLevel = TRUE, !.trap = <<>> ]
    IN
        /\\ self.trap # <<>>
        /\\ ~self.interruptLevel
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

Next == (\\E self \\in active: Step(self) \\/ Interrupt(self)) \\/ Idle
Spec == Init /\\ [][Next]_allvars

THEOREM Spec => []TypeInvariant
THEOREM Spec => [](active \subseteq (DOMAIN ctxbag))
THEOREM Spec => ((active = {}) => [](active = {}))
\* THEOREM Spec => []<>(active = {})
================""", file=f)

def usage():
    print("Usage: harmony [options] harmony-file ...")
    print("  options: ")
    print("    -a: list machine code (with labels)")
    print("    -A: list machine code (without labels)")
    print("    -B <file>.hfa: check against the given behavior")
    print("    -c name=value: define a constant")
    print("    -d: include full state into html file")
    print("    -f: run with internal model checker (not supported)")
    print("    -h: help")
    print("    -i expr: specify in interface function")
    print("    -j: list machine code in JSON format")
    print("    -m module=version: select a module version")
    print("    -o <file>: specify output file (.hvm, .hco, .hfa, .htm. .tla, .png, .gv)")
    print("    -p: parse code without running")
    print("    -s: silent (do not print periodic status updates)")
    print("    -v: print version number")
    print("    --noweb: do not automatically open web browser")
    print("    --suppress: generate less terminal output")
    exit(1)

def main():
    global silent

    # Get options.  First set default values
    consts = []
    interface = None
    mods = []
    parse_code_only = False
    printCode = None
    blockflag = False
    charmflag = True
    fulldump = False
    outputfiles = {
        "hfa": None,
        "htm": None,
        "hco": None,
        "hvm": None,
        "png": None,
        "tla": None,
        "gv":  None
    }
    testflag = False
    suppressOutput = False
    behavior = None
    charmoptions = []
    open_browser = True
    try:
        opts, args = getopt.getopt(sys.argv[1:], "AaB:bc:dfhi:jm:o:stvp",
                ["const=", "cf=", "help", "intf=", "module=", "suppress", "version", "parse", "noweb"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
    for o, a in opts:
        if o == "-a":
            printCode = "verbose"
            charmflag = False
        elif o == "--cf":
            charmoptions += [a]
        elif o == "-A":
            printCode = "terse"
            charmflag = False
        elif o == "-B":
            charmoptions += ["-B" + a]
            behavior = a
        elif o == "-j":
            printCode = "json"
            charmflag = False
        elif o == "-f":
            charmflag = False
        elif o == "-b":
            blockflag = True
        elif o in { "-c", "--const" }:
            consts.append(a)
        elif o in { "-i", "--intf" }:
            interface = a
        elif o == "-d":
            fulldump = True
        elif o in { "-m", "--module" }:
            mods.append(a)
        elif o == "-o":
            dotloc = a.rfind(".")
            if dotloc < 0:
                print("-o flag requires argument with suffix, such as x.hvm", file=sys.stderr)
                sys.exit(1)
            suffix = a[(dotloc+1):]
            if suffix not in outputfiles:
                print("unknown suffix on '%s'"%a, file=sys.stderr)
                sys.exit(1)
            elif outputfiles[suffix] != None:
                print("duplicate suffix '.%s'"%suffix, file=sys.stderr)
                sys.exit(1)
            outputfiles[suffix] = a
        elif o == "-s":
            silent = True
        elif o == "-t":
            testflag = True
        elif o in { "-h", "--help" }:
            usage()
        elif o == "--suppress":
            suppressOutput = True
        elif o in { "-v", "--version" }:
            print("Version", ".".join([str(v) for v in version]))
            sys.exit(0)
        elif o in { "-p", "--parse" }:
            parse_code_only = True
        elif o == "--noweb":
            open_browser = False
        else:
            assert False, "unhandled option"

    if args == []:
        usage()

    dotloc = args[0].rfind(".")
    if dotloc <= 0:
        usage()
    stem = args[0][:dotloc]

    if outputfiles["hvm"] == None:
        outputfiles["hvm"] = stem + ".hvm"
    if outputfiles["hco"] == None:
        outputfiles["hco"] = stem + ".hco"
    if outputfiles["htm"] == None:
        outputfiles["htm"] = stem + ".htm"
    if outputfiles["png"] != None and outputfiles["gv"] == None:
        outputfiles["gv"] = stem + ".gv"

    print("Phase 1: compile Harmony program to bytecode")
    try:
        code, scope = doCompile(args, consts, mods, interface)
    except HarmonyCompilerError as e:
        if parse_code_only:
            with open(outputfiles["hvm"], "w", encoding='utf-8') as f:
                data = {
                    "errors": [e.token._as_dict()],
                    "status": "error"
                }
                f.write(json.dumps(data, ensure_ascii=False))
        print(e.message)
        sys.exit(1)

    if parse_code_only:
        with open(outputfiles["hvm"], "w", encoding='utf-8') as f:
            f.write(json.dumps({"status": "ok"}))
        return

    if outputfiles["tla"] != None:
        with open(outputfiles["tla"], "w", encoding='utf-8') as fd:
            tla_translate(fd, code, scope)

    install_path = os.path.dirname(os.path.realpath(__file__))

    if charmflag:
        # see if there is a configuration file
        infile = "%s/charm.c"%install_path
        outfile = "%s/charm.exe"%install_path
        with open(outputfiles["hvm"], "w", encoding='utf-8') as fd:
            dumpCode("json", code, scope, f=fd)
        print("Phase 2: run the model checker")
        sys.stdout.flush()
        r = os.system("%s %s -o%s %s"%(outfile, " ".join(charmoptions), outputfiles["hco"], outputfiles["hvm"]))
        if r != 0:
            print("charm model checker failed")
            sys.exit(r)
        # TODO
        # if not testflag:
        #    os.remove(outputfiles["hvm"])
        b = Brief()
        b.run(outputfiles, behavior)
        gh = GenHTML()
        gh.run(outputfiles)
        if not suppressOutput:
            p = pathlib.Path(stem + ".htm").resolve()
            url = "file://" + str(p)
            print("open " + url + " for more information", file=sys.stderr)
            if open_browser:
                webbrowser.open(url)
        sys.exit(0)

    if printCode == None:
        (nodes, bad_node) = run(code, scope.labels, blockflag)
        if bad_node != None:
            if not silent:
                htmldump(nodes, code, scope, bad_node, fulldump, False)
            sys.exit(1)
    else:
        dumpCode(printCode, code, scope)

if __name__ == "__main__":
    main()
