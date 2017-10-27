# -*- generated by 1.0.9 -*-
import da
PatternExpr_236 = da.pat.TuplePattern([da.pat.ConstantPattern('finish'), da.pat.FreePattern('client_res')])
PatternExpr_243 = da.pat.FreePattern('client')
PatternExpr_293 = da.pat.TuplePattern([da.pat.ConstantPattern('parent-trans'), da.pat.FreePattern('encrypt_oper'), da.pat.FreePattern('encrypt_rid')])
PatternExpr_302 = da.pat.FreePattern('client')
_config_object = {}
import sys
import nacl.encoding
import nacl.hash
import nacl.signing
from nacl.bindings.utils import sodium_memcmp
from re import split
import time
import logging

class Parent(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_ParentReceivedEvent_0', PatternExpr_236, sources=[PatternExpr_243], destinations=None, timestamps=None, record_history=None, handlers=[self._Parent_handler_235]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ParentReceivedEvent_1', PatternExpr_293, sources=[PatternExpr_302], destinations=None, timestamps=None, record_history=None, handlers=[self._Parent_handler_292])])

    def setup(self, c, public_key_dict, pk, **rest_480):
        super().setup(c=c, public_key_dict=public_key_dict, pk=pk, **rest_480)
        self._state.c = c
        self._state.public_key_dict = public_key_dict
        self._state.pk = pk
        self._state.d = dict()
        self._state.result = dict()

    def run(self):
        logging.basicConfig(format='%(asctime)s : %(message)s', level=logging.INFO, filename=(sys.argv[(- 1)][0:(- 4)] + '_log.log'))
        res = ''
        super()._label('_st_label_231', block=False)
        _st_label_231 = 0
        while (_st_label_231 == 0):
            _st_label_231 += 1
            if False:
                _st_label_231 += 1
            else:
                super()._label('_st_label_231', block=True)
                _st_label_231 -= 1

    def _Parent_handler_235(self, client_res, client):
        if (not (self._state.result[client] == client_res)):
            logging.error(((((('Parent Client : Final Results check failed for Client : ' + str(self._state.c.index(client))) + ' parent res ') + str(self._state.result[client])) + ' client res ') + str(client_res)))
        else:
            logging.info(('Parent Client : Final Results check passed for Client : ' + str(self._state.c.index(client))))
    _Parent_handler_235._labels = None
    _Parent_handler_235._notlabels = None

    def _Parent_handler_292(self, encrypt_oper, encrypt_rid, client):
        cl_parent_dkey = nacl.signing.VerifyKey(self._state.public_key_dict[client], encoder=nacl.encoding.HexEncoder)
        try:
            cl_parent_dkey.verify(encrypt_oper)
        except nacl.exceptions.BadSignatureError:
            self.output('fr-r decrypt fail')
        oper = encrypt_oper.message.decode()
        x = split("[,()']+", oper)
        if (x[0] == 'put'):
            self._state.d[x[1]] = x[2]
            res = 'ok'
        if (x[0] == 'get'):
            try:
                res = self._state.d[x[1]]
            except KeyError:
                res = ''
        if (x[0] == 'append'):
            try:
                self._state.d[x[1]] = (self._state.d[x[1]] + x[2])
                res = 'update ok'
            except KeyError:
                res = 'update failed'
        if (x[0] == 'slice'):
            x[2] = x[2].split(':')
            try:
                self._state.d[x[1]] = self._state.d[x[1]][int(x[2][0]):int(x[2][1])]
                res = 'slice ok'
            except KeyError:
                res = 'slice fail'
        try:
            self._state.result[client].append(res)
        except KeyError:
            self._state.result[client] = [res]
    _Parent_handler_292._labels = None
    _Parent_handler_292._notlabels = None