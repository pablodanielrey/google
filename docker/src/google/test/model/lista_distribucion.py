from google.model.GoogleAuthApi import GAuthApis

def obtenerPlatantilla(name, email):
    return {
            'name': name,
            'archiveOnly': 'false',
            'whoCanAdd': 'ALL_MANAGERS_CAN_ADD',
            'includeCustomFooter': 'false',
            'spamModerationLevel': 'MODERATE',
            'whoCanContactOwner': 'ANYONE_CAN_CONTACT',
            'allowWebPosting': 'true',
            'customFooterText': '',
            'kind': 'groupsSettings#groups',
            'whoCanViewGroup': 'ALL_IN_DOMAIN_CAN_VIEW',
            'email': email,
            'membersCanPostAsTheGroup': 'false',
            'whoCanInvite': 'ALL_MEMBERS_CAN_INVITE',
            'messageDisplayFont': 'DEFAULT_FONT',
            'replyTo': 'REPLY_TO_IGNORE',
            'whoCanViewMembership': 'ALL_MANAGERS_CAN_VIEW',
            'showInGroupDirectory': 'false',
            'whoCanJoin': 'ALL_IN_DOMAIN_CAN_JOIN',
            'allowGoogleCommunication': 'false',
            'includeInGlobalAddressList': 'true',
            'isArchived': 'true',
            'whoCanLeaveGroup': 'ALL_MEMBERS_CAN_LEAVE',
            'description': name,
            'sendMessageDenyNotification': 'false',
            'allowExternalMembers': 'false',
            'customReplyTo': '',
            'messageModerationLevel': 'MODERATE_NONE',
            'defaultMessageDenyNotificationText': '',
            'maxMessageBytes': 26214400,
            'whoCanPostMessage': 'ALL_MANAGERS_CAN_POST'}



if __name__ == '__main__':
    SCOPES = ['https://www.googleapis.com/auth/apps.groups.settings']
    version='v1'
    api='groupssettings'
    userId = '31381082@econo.unlp.edu.ar'

    name = "Nueva lista de distribucion"
    groupEmail = 'nueva_lista@econo.unlp.edu.ar'

    service = GAuthApis.getService(version, api, SCOPES, userId)
    try:
        # results = service.groups().get(groupUniqueId=groupEmail).execute()
        # print(results)
        print(obtenerPlatantilla(name, groupEmail))
    except:
        print('Unable to read group: {0}'.format(groupEmail))
        raise
