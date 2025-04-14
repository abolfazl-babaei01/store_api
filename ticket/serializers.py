from rest_framework import serializers
from .models import Ticket, TicketMessage


class TicketListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing tickets with a link to their detail view.
    """
    detail_url = serializers.HyperlinkedIdentityField(
        view_name='ticket:ticket_detail',  # The name of the URL pattern for ticket detail view
        lookup_field='pk',                 # Use the primary key to look up the object
        read_only=True                     # This field is for display only
    )

    class Meta:
        model = Ticket
        fields = ['id', 'subject', 'is_blocked', 'created_at', 'detail_url']


class TicketMessageSerializer(serializers.ModelSerializer):
    """
    Serializer for individual messages in a ticket, including sender's full name.
    """
    sender = serializers.SlugRelatedField(
        slug_field='get_full_name',  # Show sender's full name
        read_only=True               # Sender is not editable via the API
    )

    class Meta:
        model = TicketMessage
        fields = ['id', 'sender', 'text', 'created_at']


class TicketDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for ticket detail including its related messages.
    """
    messages = TicketMessageSerializer(source='messages.all', many=True)  # All messages for this ticket

    class Meta:
        model = Ticket
        fields = ['id', 'subject', 'created_at', 'messages']


class TicketCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new ticket and its first message.
    """
    text = serializers.CharField(write_only=True)  # Initial message text

    class Meta:
        model = Ticket
        fields = ['id', 'subject', 'text']

    def create(self, validated_data):
        user = self.context['request'].user
        text = validated_data.pop('text')

        # Create the ticket
        ticket = Ticket.objects.create(user=user, **validated_data)

        # Create the first message for the ticket
        TicketMessage.objects.create(
            ticket=ticket,
            sender=user,
            text=text,
        )
        return ticket


class TicketMessageCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for adding a message to an existing ticket.
    """
    class Meta:
        model = TicketMessage
        fields = ['id', 'ticket', 'text']

    def validate(self, data):
        """
        Ensure the user is allowed to reply to the specified ticket.
        """
        user = self.context['request'].user
        ticket = data['ticket']

        try:
            ticket = Ticket.objects.get(id=ticket.id)
        except Ticket.DoesNotExist:
            raise serializers.ValidationError('Ticket does not exist')

        if ticket.user != user:
            raise serializers.ValidationError('You do not have permission to reply to this ticket.')

        # check ticket is blocked or no
        if ticket.is_blocked:
            raise serializers.ValidationError('This ticket is blocked.')

        return data

    def create(self, validated_data):
        """
        Set the sender to the current user before saving the message.
        """
        user = self.context['request'].user
        validated_data['sender'] = user
        return super().create(validated_data)
