from docusign_rooms import FieldDataForCreate, RolesApi, RoomsApi, RoomForCreate, RoomTemplatesApi
from flask import session, request

from ...utils import create_rooms_api_client


class Eg002Controller:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        return {
            "account_id": session["ds_account_id"],  # Represents your {ACCOUNT_ID}
            "access_token": session["ds_access_token"],  # Represents your {ACCESS_TOKEN}
            "room_name": request.form.get("room_name"),
            "template_id": request.form.get("template_id"),
        }

    @staticmethod
    def get_templates(args):
        """
        1. Create an API client with headers
        2. Get room templates
        """
        # Step 1. Create an API client with headers
        api_client = create_rooms_api_client(access_token=args["access_token"])

        # Step 2. Get room templates
        room_templates_api = RoomTemplatesApi(api_client)
        templates = room_templates_api.get_room_templates(account_id=args["account_id"])
        return templates.room_templates

    @staticmethod
    def worker(args):
        """
        1. Create an API client with headers
        2. Get Default Admin role id
        3. Create RoomForCreate object
        4. Post the room using SDK
        """
        # Step 1. Create an API client with headers
        api_client = create_rooms_api_client(access_token=args["access_token"])

        # Step 2. Get Default Admin role id
        roles_api = RolesApi(api_client)
        roles = roles_api.get_roles(account_id=args["account_id"])
        role_id = [role.role_id for role in roles.roles if role.is_default_for_admin][0]

        # Step 3. Create RoomForCreate object
        room = RoomForCreate(
            name=args["room_name"],
            role_id=role_id,
            template_id=args['template_id'],
            field_data=FieldDataForCreate(
                data={
                    'address1': '123 EZ Street',
                    'city': 'Galaxian',
                    'state': 'US-HI',
                    'postalCode': '11111',
                }
            )
        )

        # Step 4. Post the room using SDK
        rooms_api = RoomsApi(api_client)
        response = rooms_api.create_room(
            room_for_create=room,
            account_id=args["account_id"],
        )
        return response
