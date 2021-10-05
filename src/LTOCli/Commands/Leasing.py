from LTOCli import HandleDefault as handle
from LTO.Transactions.Lease import Lease
from LTO.Transactions.CancelLease import CancelLease
from LTOCli import Config
from LTO.PublicNode import PublicNode
import json


def func(nameSpace, parser):
    if vars(nameSpace)['subparser-name-lease'] == 'create':
        transaction = Lease(recipient=nameSpace.recipient[0], amount=nameSpace.amount[0])
        transaction.signWith(handle.getAccount(parser))
        if vars(nameSpace)['unsigned'] is False:
            if vars(nameSpace)['account']:
                transaction.signWith(handle.getAccountFromOption(parser, vars(nameSpace)['account'][0]))
            else:
                transaction.signWith(handle.getAccount(parser))
            if vars(nameSpace)['no_broadcast'] is False:
                transaction = transaction.broadcastTo(handle.getNode())
        elif vars(nameSpace)['no_broadcast'] is False:
            parser.error(
                "Use the '--unsigned' option only in combination with the '--no-broadcast' option. Type 'lto lease create --help' for more informations ")
        handle.prettyPrint(transaction)

    elif vars(nameSpace)['subparser-name-lease'] == 'cancel':
        transaction = CancelLease(leaseId=nameSpace.leaseId[0])
        transaction.signWith(handle.getAccount(parser))
        if vars(nameSpace)['unsigned'] is False:
            if vars(nameSpace)['account']:
                transaction.signWith(handle.getAccountFromOption(parser, vars(nameSpace)['account'][0]))
            else:
                transaction.signWith(handle.getAccount(parser))
            if vars(nameSpace)['no_broadcast'] is False:
                transaction = transaction.broadcastTo(handle.getNode())
        elif vars(nameSpace)['no_broadcast'] is False:
            parser.error(
                "Use the '--unsigned' option only in combination with the '--no-broadcast' option. Type 'lto lease cancel --help' for more informations ")
        handle.prettyPrint(transaction)







    elif vars(nameSpace)['subparser-name-lease'] == 'list':  # The lease that I'm giving

        node = PublicNode('http://testnet.lto.network')

        if vars(nameSpace)['account']:
            address = handle.getAccountFromOption(parser, vars(nameSpace)['account'][0]).address
        else:
            address = handle.getAccount(parser).address


        def leaseList(address):
            return node.wrapper(api='/leasing/active/{}'.format(address))

        value = leaseList(address)
        flag = 0
        for x in value:
            if x['sender'] == address:  # outbound
                print(x['sender'], ':', x['amount'])
                flag +=1
        if flag == 0:
            print("No outbound lease found")

    elif vars(nameSpace)['subparser-name-lease'] == 'list-inbound':  # The lease that I've received

        node = PublicNode('http://testnet.lto.network')

        if vars(nameSpace)['account']:
            address = handle.getAccountFromOption(parser, vars(nameSpace)['account'][0]).address
        else:
            address = handle.getAccount(parser).address

        def leaseList(address):
            return node.wrapper(api='/leasing/active/{}'.format(address))

        value = leaseList(address)
        flag = 0
        for x in value:
            if x['recipient'] == address:  # inbound
                print(x['sender'], ':', x['amount'])
                flag +=1
        if flag == 0:
            print("No inbound lease found")

    else:
        parser.error('Type lto lease --help for instructions')
