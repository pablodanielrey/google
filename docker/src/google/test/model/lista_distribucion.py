from google.model.GoogleAuthApi import GAuthApis
import sys, os

def obtenerPlatantilla(name, email, replyTo):
    return {
            'whoCanContactOwner': 'ANYONE_CAN_CONTACT',
            'includeInGlobalAddressList': 'true',
            'allowGoogleCommunication': 'false',
            'messageDisplayFont': 'DEFAULT_FONT',
            'sendMessageDenyNotification': 'false',
            'archiveOnly': 'false',
            'customReplyTo': replyTo,
            'replyTo': 'REPLY_TO_CUSTOM',
            'membersCanPostAsTheGroup': 'false',
            'kind': 'groupsSettings#groups',
            'whoCanJoin': 'INVITED_CAN_JOIN',
            'showInGroupDirectory': 'false',
            'spamModerationLevel': 'MODERATE',
            'email': email,
            'whoCanViewGroup': 'ALL_MEMBERS_CAN_VIEW',
            'isArchived': 'true',
            'whoCanInvite': 'ALL_MANAGERS_CAN_INVITE',
            'maxMessageBytes': 26214400,
            'name': name,
            'defaultMessageDenyNotificationText': '',
            'whoCanPostMessage': 'ALL_MANAGERS_CAN_POST',
            'whoCanLeaveGroup': 'ALL_MEMBERS_CAN_LEAVE',
            'customFooterText': '',
            'description': name,
            'primaryLanguage': 'es',
            'whoCanViewMembership': 'ALL_MANAGERS_CAN_VIEW',
            'allowExternalMembers': 'true',
            'allowWebPosting': 'true',
            'messageModerationLevel': 'MODERATE_NONE',
            'includeCustomFooter': 'false',
            'whoCanAdd': 'ALL_MANAGERS_CAN_ADD'}



def crearGrupo(userId, name, email):
    SCOPES = ['https://www.googleapis.com/auth/admin.directory.group']
    service = GAuthApis.getService('directory_v1', 'admin', SCOPES, userId)
    return service.groups().insert(body={'name':name, 'email':email}).execute()



if __name__ == '__main__':
    SCOPES = ['https://www.googleapis.com/auth/apps.groups.settings']
    version='v1'
    api='groupssettings'
    userId = os.environ['ADMIN_USER_GOOGLE']

    name = sys.argv[1]
    groupEmail = sys.argv[2]
    replyTo = sys.argv[3]

    service = GAuthApis.getService(version, api, SCOPES, userId)
    try:
        crearGrupo(userId, name, groupEmail)
        newGroup = obtenerPlatantilla(name, groupEmail, replyTo)
        results = service.groups().update(groupUniqueId=groupEmail, body=newGroup).execute()
        print(results)
    except:
        print('Unable to read group: {0}'.format(groupEmail))
        raise
